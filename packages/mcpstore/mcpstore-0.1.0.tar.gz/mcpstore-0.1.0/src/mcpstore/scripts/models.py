from enum import Enum
from typing import Dict, Any, Optional, List, Literal, Union
from pydantic import BaseModel, Field, HttpUrl, validator
import os
from datetime import datetime

class TransportType(str, Enum):
    """传输类型枚举，与 FastMCP 的传输类型名称匹配"""
    STREAMABLE_HTTP = "streamable-http"
    SSE = "sse"
    PYTHON_STDIO = "python-stdio"
    NODE_STDIO = "node-stdio"
    UVX_STDIO = "uvx-stdio"
    NPX_STDIO = "npx-stdio"

class BaseRegisterRequest(BaseModel):
    """注册请求的基础模型"""
    name: str = ""  # 服务名称，如果为空则自动生成
    env: Optional[Dict[str, str]] = None  # 环境变量配置
    keep_alive: bool = True  # 会话持久化选项

    @validator('name')
    def validate_name(cls, v):
        if v and not v.replace('_', '').replace('-', '').isalnum():
            raise ValueError("Service name can only contain letters, numbers, underscores and hyphens")
        return v

    @validator('env')
    def validate_env(cls, v):
        if v is not None:
            # 验证环境变量名称格式
            for key in v.keys():
                if not key.replace('_', '').isalnum():
                    raise ValueError(f"Invalid environment variable name: {key}")
        return v

class HTTPRegisterRequest(BaseRegisterRequest):
    """HTTP/SSE 服务注册请求模型"""
    url: HttpUrl  # 服务URL
    transport_type: Literal[TransportType.STREAMABLE_HTTP, TransportType.SSE] = TransportType.STREAMABLE_HTTP
    headers: Optional[Dict[str, str]] = None  # 自定义请求头

class StdioRegisterRequest(BaseRegisterRequest):
    """本地脚本服务注册请求模型"""
    script_path: str  # 脚本路径
    command: Optional[str] = None  # 可选的命令
    args: Optional[List[str]] = None  # 命令行参数
    transport_type: Literal[TransportType.PYTHON_STDIO, TransportType.NODE_STDIO]
    working_dir: Optional[str] = None  # 工作目录
    
    @validator('script_path')
    def validate_script_path(cls, v, values):
        if not v.endswith(('.py', '.js')):
            raise ValueError("Script path must end with .py or .js")
        
        # 验证文件是否存在
        if not os.path.exists(v):
            raise ValueError(f"Script file not found: {v}")
            
        # 验证文件扩展名与传输类型匹配
        if values.get('transport_type') == TransportType.PYTHON_STDIO and not v.endswith('.py'):
            raise ValueError("Python transport requires a .py file")
        if values.get('transport_type') == TransportType.NODE_STDIO and not v.endswith('.js'):
            raise ValueError("Node transport requires a .js file")
            
        return v

class ToolRegisterRequest(BaseRegisterRequest):
    """工具服务注册请求模型"""
    tool_name: str  # 工具名称
    args: Optional[List[str]] = None  # 工具参数
    transport_type: Literal[TransportType.UVX_STDIO, TransportType.NPX_STDIO]
    package_name: Optional[str] = None  # NPX 包名

# 用于统一接口的联合类型
RegisterRequestUnion = Union[HTTPRegisterRequest, StdioRegisterRequest, ToolRegisterRequest]




class ToolInfo(BaseModel):
    """工具信息"""
    name: str
    description: str
    service_name: Optional[str] = None
    client_id: Optional[str] = None  # 关联的client_id
    inputSchema: Optional[Dict[str, Any]] = None

class ServiceInfo(BaseModel):
    """服务信息模型"""
    url: str = ""  # URL 默认为空字符串
    name: str
    transport_type: TransportType
    status: Literal["healthy", "unhealthy"]
    tool_count: int
    keep_alive: bool
    working_dir: Optional[str] = None
    env: Optional[Dict[str, str]] = None
    last_heartbeat: Optional[datetime] = None
    command: Optional[str] = None  # 命令（用于 STDIO 服务）
    args: Optional[List[str]] = None  # 参数列表（用于 STDIO 服务）
    package_name: Optional[str] = None  # NPX 包名（用于 NPX 服务）

class ServicesResponse(BaseModel):
    """服务列表响应模型"""
    services: List[ServiceInfo]
    total_services: int
    total_tools: int
    
class ToolsResponse(BaseModel):
    """工具列表响应"""
    tools: List[ToolInfo]
    total_tools: int 

class JsonRegisterRequest(BaseModel):
    """JSON注册请求模型"""
    config: Dict[str, Any] = Field(..., description="MCP服务配置字典")
    client_id: Optional[str] = Field(None, description="客户端ID，如果不提供则自动生成")

class ServiceRegistrationResult(BaseModel):
    """服务注册结果模型"""
    status: Literal["success", "failed"]
    message: str
    error: Optional[str] = None

class JsonRegistrationResponse(BaseModel):
    """JSON注册响应模型"""
    client_id: str
    services: Dict[str, ServiceRegistrationResult]
    total_success: int
    total_failed: int

class JsonUpdateRequest(BaseModel):
    """JSON更新请求模型"""
    config: Dict[str, Any] = Field(..., description="完整的MCP服务配置字典")
    client_id: Optional[str] = Field(None, description="客户端ID，默认使用main_client")

class JsonConfigResponse(BaseModel):
    """JSON配置响应模型"""
    client_id: str
    config: Dict[str, Any]

