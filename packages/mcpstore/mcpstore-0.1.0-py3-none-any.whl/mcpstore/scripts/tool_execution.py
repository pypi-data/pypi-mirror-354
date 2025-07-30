from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any, Optional, Union, List
from mcpstore.core.orchestrator import MCPOrchestrator
from mcpstore.core.registry import ServiceRegistry
from mcpstore.scripts.deps import get_orchestrator, get_registry
from pydantic import BaseModel, Field
import logging
import asyncio
from enum import Enum
from mcpstore.scripts.models import ToolExecutionRequest, ToolExecutionResponse, ContentUnion

router = APIRouter()
logger = logging.getLogger(__name__)

class ContentType(str, Enum):
    """内容类型枚举"""
    TEXT = "text"
    IMAGE = "image"
    JSON = "json"
    BINARY = "binary"

class Content(BaseModel):
    """基础内容模型"""
    type: ContentType
    mime_type: Optional[str] = None

class TextContent(Content):
    """文本内容"""
    type: ContentType = ContentType.TEXT
    text: str

class ImageContent(Content):
    """图像内容"""
    type: ContentType = ContentType.IMAGE
    url: str
    alt: Optional[str] = None

class JsonContent(Content):
    """JSON内容"""
    type: ContentType = ContentType.JSON
    data: Dict[str, Any]

class BinaryContent(Content):
    """二进制内容"""
    type: ContentType = ContentType.BINARY
    data: bytes
    filename: Optional[str] = None

ContentUnion = Union[TextContent, ImageContent, JsonContent, BinaryContent]

class ToolExecutionRequest(BaseModel):
    """工具执行请求模型"""
    tool_name: str
    parameters: Dict[str, Any]
    timeout: Optional[float] = Field(None, description="执行超时时间(秒)")

class ToolExecutionResponse(BaseModel):
    """工具执行响应模型"""
    result: Optional[List[ContentUnion]] = None
    status: str = "success"
    error: Optional[str] = None

@router.post("/execute", response_model=ToolExecutionResponse)
async def execute_tool(
    request: ToolExecutionRequest,
    orchestrator: MCPOrchestrator = Depends(get_orchestrator),
    registry: ServiceRegistry = Depends(get_registry)
):
    """执行工具
    
    Args:
        request: 工具执行请求
            - tool_name: 工具名称
            - parameters: 工具参数
            - timeout: 可选的超时时间(秒)
    """
    try:
        # 1. 验证工具是否存在
        tool_info = None
        for tool in registry.get_all_tool_info():
            if tool["name"] == request.tool_name:
                tool_info = tool
                break
                
        if not tool_info:
            raise HTTPException(
                status_code=404,
                detail=f"Tool not found: {request.tool_name}"
            )
            
        # 2. 获取服务信息
        service_name = tool_info["service_name"]
        if not service_name:
            raise HTTPException(
                status_code=500,
                detail=f"Service not found for tool: {request.tool_name}"
            )
            
        # 3. 验证服务健康状态
        is_healthy = await orchestrator.is_service_healthy(service_name)
        if not is_healthy:
            raise HTTPException(
                status_code=503,
                detail=f"Service {service_name} is unhealthy"
            )
            
        # 4. 验证参数
        input_schema = tool_info.get("inputSchema")
        if input_schema:
            # TODO: 实现参数验证
            pass
            
        # 5. 执行工具(带超时)
        try:
            if request.timeout:
                # 使用 asyncio.wait_for 实现超时
                result = await asyncio.wait_for(
                    orchestrator.execute_tool(
                        service_name=service_name,
                        tool_name=request.tool_name,
                        parameters=request.parameters
                    ),
                    timeout=request.timeout
                )
            else:
                result = await orchestrator.execute_tool(
                    service_name=service_name,
                    tool_name=request.tool_name,
                    parameters=request.parameters
                )
            
            # 处理结果，转换为适当的内容类型
            processed_results = []
            if isinstance(result, (list, tuple)):
                for item in result:
                    processed_results.extend(process_result_item(item))
            else:
                processed_results.extend(process_result_item(result))
            
            return ToolExecutionResponse(
                result=processed_results,
                status="success"
            )
            
        except asyncio.TimeoutError:
            logger.error(f"Tool execution timed out after {request.timeout} seconds")
            return ToolExecutionResponse(
                result=None,
                status="error",
                error=f"Execution timed out after {request.timeout} seconds"
            )
            
        except Exception as e:
            logger.error(f"Tool execution failed: {e}", exc_info=True)
            return ToolExecutionResponse(
                result=None,
                status="error",
                error=str(e)
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error during tool execution: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

def process_result_item(item: Any) -> List[ContentUnion]:
    """处理单个结果项，转换为适当的内容类型"""
    if isinstance(item, str):
        return [TextContent(text=item)]
    elif isinstance(item, bytes):
        return [BinaryContent(data=item)]
    elif isinstance(item, dict):
        return [JsonContent(data=item)]
    elif isinstance(item, (list, tuple)):
        results = []
        for sub_item in item:
            results.extend(process_result_item(sub_item))
        return results
    else:
        # 尝试转换为字符串
        return [TextContent(text=str(item))] 
