from fastapi import APIRouter, Depends, HTTPException, Path
from typing import Dict, Any, Optional, List
from mcpstore.core.registry import ServiceRegistry
from mcpstore.core.orchestrator import MCPOrchestrator
from mcpstore.scripts.models import (
    TransportType, 
    HTTPRegisterRequest, 
    StdioRegisterRequest, 
    ToolRegisterRequest,
    RegisterRequestUnion,
    ServiceInfo,
    ServicesResponse,
    ToolInfo,
    ToolsResponse,
    JsonRegisterRequest,
    JsonRegistrationResponse,
    ServiceRegistrationResult,
    JsonUpdateRequest,
    JsonConfigResponse
)
from mcpstore.scripts.deps import get_orchestrator, get_registry
import logging
import time
import json
import os
from mcpstore.scripts.client_registration import load_client_configs, load_agent_clients

router = APIRouter()
logger = logging.getLogger(__name__)

async def _process_registration(
    payload: RegisterRequestUnion,
    orchestrator: MCPOrchestrator,
    agent_id: Optional[str] = None
) -> Dict[str, str]:
    """统一的注册处理逻辑，使用官方方法添加服务到mcp.json并重新加载"""
    try:
        # 构建符合官方格式的服务配置
        service_name = payload.name or f"service_{int(time.time())}"
        service_config = {}
        
        # 根据不同类型的请求添加特定配置
        if isinstance(payload, HTTPRegisterRequest):
            service_config = {
                "url": str(payload.url),
                "transport": payload.transport_type,
                "headers": payload.headers or {}
            }
        elif isinstance(payload, StdioRegisterRequest):
            if payload.transport_type == TransportType.PYTHON_STDIO:
                service_config = {
                    "command": payload.command or "python",
                    "args": [payload.script_path] + (payload.args or []),
                    "env": payload.env or {},
                    "working_dir": payload.working_dir
                }
            elif payload.transport_type == TransportType.NODE_STDIO:
                service_config = {
                    "command": payload.command or "node",
                    "args": [payload.script_path] + (payload.args or []),
                    "env": payload.env or {},
                    "working_dir": payload.working_dir
                }
        elif isinstance(payload, ToolRegisterRequest):
            if payload.transport_type == TransportType.UVX_STDIO:
                service_config = {
                    "command": "uvx",
                    "args": [payload.tool_name] + (payload.args or []),
                    "env": payload.env or {}
                }
            elif payload.transport_type == TransportType.NPX_STDIO:
                service_config = {
                    "command": "npx",
                    "args": [(payload.package_name or payload.tool_name)] + (payload.args or []),
                    "env": payload.env or {}
                }
        
        # 添加服务配置到mcp.json
        # 获取当前配置
        current_config = orchestrator.mcp_config.load_config()
        if "mcpServers" not in current_config:
            current_config["mcpServers"] = {}
            
        # 添加新服务
        current_config["mcpServers"][service_name] = service_config
        
        # 保存配置
        ok = orchestrator.mcp_config.save_config(current_config)
        if not ok:
            raise Exception("Failed to save service configuration")
            
        # 重新加载所有服务
        await orchestrator.load_from_config()
        
        # 如果指定了agent_id，为该agent更新client
        if agent_id:
            if agent_id in orchestrator.agent_clients:
                # 为特定agent创建新的client
                agent_client = orchestrator.main_client
                orchestrator.agent_clients[agent_id] = agent_client
                logger.info(f"Updated client for agent {agent_id}")
            else:
                # 如果agent不存在，创建新的agent client
                agent_client = await orchestrator.register_agent_client(agent_id)
                if not agent_client:
                    logger.warning(f"Failed to register agent client: {agent_id}")
        
        # 检查服务是否健康
        is_healthy = await orchestrator.is_service_healthy(service_name)
        
        if is_healthy:
            # 获取工具数量
            tools = orchestrator.registry.get_tools_for_service(service_name)
            tool_count = len(tools)
            message = f"Service {service_name} registered successfully with {tool_count} tools"
            if agent_id:
                message += f" and connected to agent {agent_id}"
            logger.info(message)
            return {"status": "success", "message": message}
        else:
            logger.error(f"Service {service_name} registration failed: service is unhealthy")
            # 处理特定的错误情况
            orchestrator.pending_reconnection.add(service_name)
            raise HTTPException(status_code=502, detail=f"Service {service_name} is unhealthy after registration")
            
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Unexpected error during registration: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error during registration: {str(e)}"
        )

# 统一注册接口
@router.post("/register", response_model=Dict[str, str])
async def register_service(
    payload: RegisterRequestUnion,
    agent_id: Optional[str] = None,
    orchestrator: MCPOrchestrator = Depends(get_orchestrator)
):
    """
    统一的服务注册接口，支持所有类型的服务注册
    
    - payload: 服务注册请求
    - agent_id: 可选的agent ID，指定要将服务注册到哪个agent
    """
    return await _process_registration(payload, orchestrator, agent_id)

# 删除特定类型注册接口
# @router.post("/register/http", response_model=Dict[str, str])
# async def register_http_service(
#     payload: HTTPRegisterRequest,
#     orchestrator: MCPOrchestrator = Depends(get_orchestrator)
# ):
#     """HTTP/SSE服务专用注册接口"""
#     return await _process_registration(payload, orchestrator)

# @router.post("/register/stdio", response_model=Dict[str, str])
# async def register_stdio_service(
#     payload: StdioRegisterRequest,
#     orchestrator: MCPOrchestrator = Depends(get_orchestrator)
# ):
#     """本地脚本服务专用注册接口"""
#     return await _process_registration(payload, orchestrator)

# @router.post("/register/tool", response_model=Dict[str, str])
# async def register_tool_service(
#     payload: ToolRegisterRequest,
#     orchestrator: MCPOrchestrator = Depends(get_orchestrator)
# ):
#     """工具服务专用注册接口"""
#     return await _process_registration(payload, orchestrator)

def read_mcp_json() -> Dict[str, Any]:
    """读取默认的mcp.json文件"""
    try:
        with open("@mcp.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to read @mcp.json: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to read @mcp.json: {str(e)}"
        )

@router.post("/register/json", response_model=JsonRegistrationResponse)
async def register_json_service(
    client_id: Optional[str] = None,
    service_names: Optional[List[str]] = None,
    orchestrator: MCPOrchestrator = Depends(get_orchestrator)
):
    """
    注册服务，支持 main_client 和普通 client
    - client_id: 客户端ID，若为 main_client 则注册主客户端，否则注册普通客户端
    - service_names: 普通 client 时可指定服务名列表
    """
    try:
        if client_id == orchestrator.client_manager.main_client_id or not client_id:
            # main_client 注册，读取 mcp.json
            config = orchestrator.mcp_config.load_config()
        else:
            # 普通 client 注册，根据服务名列表生成 config
            if not service_names:
                raise HTTPException(status_code=400, detail="service_names required for non-main_client registration")
            config = orchestrator.create_client_config_from_names(service_names)
        results = await orchestrator.register_json_services(config, client_id=client_id)
        return JsonRegistrationResponse(
            client_id=results["client_id"],
            services={},  # 可扩展为详细注册结果
            total_success=results["total_services"],
            total_failed=0 if results["status"] == "success" else 1
        )
    except Exception as e:
        logger.error(f"Error during JSON registration: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error during registration: {str(e)}"
        )

@router.put("/register/json", response_model=JsonRegistrationResponse)
async def update_json_service(
    payload: JsonUpdateRequest,
    orchestrator: MCPOrchestrator = Depends(get_orchestrator)
):
    """
    使用提供的配置更新服务
    
    Args:
        payload: JSON更新请求
        orchestrator: MCP编排器实例
    """
    try:
        # 调用注册方法（更新实际上是重新注册）
        results = await orchestrator.register_json_services(
            config=payload.config,
            client_id=payload.client_id
        )
        
        # 转换结果为响应模型
        return JsonRegistrationResponse(
            client_id=results["client_id"],
            services={
                name: ServiceRegistrationResult(**result) 
                if isinstance(result, dict) else result
                for name, result in results["services"].items()
            },
            total_success=results["total_success"],
            total_failed=results["total_failed"]
        )
        
    except Exception as e:
        logger.error(f"Error during JSON update: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error during update: {str(e)}"
        )

@router.get("/register/json", response_model=JsonConfigResponse)
async def get_json_config(
    client_id: Optional[str] = None,
    orchestrator: MCPOrchestrator = Depends(get_orchestrator)
):
    """
    查询服务配置，支持 main_client 和普通 client
    - client_id: 客户端ID，若为 main_client 则查询主客户端配置，否则查询普通客户端配置
    """
    try:
        if not client_id or client_id == orchestrator.client_manager.main_client_id:
            config = orchestrator.mcp_config.load_config()
            return JsonConfigResponse(
                client_id=orchestrator.client_manager.main_client_id,
                config=config
            )
        else:
            config = orchestrator.client_manager.get_client_config(client_id)
            if not config:
                raise HTTPException(
                    status_code=404,
                    detail=f"Client configuration not found: {client_id}"
                )
            return JsonConfigResponse(
                client_id=client_id,
                config=config
            )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting JSON config: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error getting config: {str(e)}"
        )

@router.get("/health", response_model=Dict[str, Any])
async def get_health_status(
    registry: ServiceRegistry = Depends(get_registry),
    orchestrator: MCPOrchestrator = Depends(get_orchestrator)
):
    """获取服务健康状态"""
    services = []
    for name, config in orchestrator.mcp_config.load_config().get("mcpServers", {}).items():
        # 获取服务的真实健康状态
        is_healthy = await orchestrator.is_service_healthy(name)
        
        # 构建服务状态信息
        service_status = {
            "name": name,
            "url": config.get("url", ""),  # 如果没有 URL，则为空字符串
            "transport_type": infer_transport_type(config),
            "status": "healthy" if is_healthy else "unhealthy",
            "command": config.get("command"),  # 添加命令信息
            "args": config.get("args"),  # 添加参数列表
            "package_name": config.get("package_name")  # 添加包名信息
        }
        services.append(service_status)
        
    return {
        "orchestrator_status": "running",
        "active_services": registry.get_session_count(),
        "total_tools": registry.get_tool_count(),
        "services": services
    }

@router.get("/service_info", response_model=Dict[str, Any])
async def get_service_info(
    name: str,
    registry: ServiceRegistry = Depends(get_registry),
    orchestrator: MCPOrchestrator = Depends(get_orchestrator)
):
    """获取服务的详细信息
    
    Args:
        name: 服务名称
    """
    if not registry.has_service(name):
        raise HTTPException(status_code=404, detail=f"Service not found: {name}")
        
    # 获取基本服务信息
    service_info = registry.get_service_info(name)
    
    # 获取服务配置
    config = orchestrator.mcp_config.get_service_config(name)
    if config:
        # 添加配置信息到返回结果
        service_info.update({
            "url": config.get("url", ""),  # 如果没有 URL，则为空字符串
            "transport_type": infer_transport_type(config),
            "keep_alive": infer_keep_alive(config),
            "working_dir": config.get("working_dir"),
            "env": config.get("env"),
            "command": config.get("command"),  # 添加命令信息
            "args": config.get("args"),  # 添加参数列表
            "package_name": config.get("package_name")  # 添加包名信息
        })
    
    # 检查服务健康状态
    is_healthy = await orchestrator.is_service_healthy(name)
    service_info["status"] = "healthy" if is_healthy else "unhealthy"
    
    return service_info

def infer_transport_type(service_config):
    if not service_config:
        return TransportType.STREAMABLE_HTTP
    # 优先使用 transport 字段
    transport = service_config.get("transport")
    if transport:
        return transport
    # 其次根据 url 判断
    if service_config.get("url"):
        return TransportType.STREAMABLE_HTTP
    # 根据 command/args 判断
    cmd = (service_config.get("command") or "").lower()
    args = " ".join(service_config.get("args", [])).lower()
    if "python" in cmd or ".py" in args:
        return TransportType.PYTHON_STDIO
    if "node" in cmd or ".js" in args:
        return TransportType.NODE_STDIO
    # 其它可扩展
    return TransportType.STREAMABLE_HTTP

def infer_keep_alive(service_config):
    # 目前所有服务默认 keep_alive True，可根据需要扩展
    return True

@router.get("/services", response_model=ServicesResponse)
async def list_services(
    registry: ServiceRegistry = Depends(get_registry),
    orchestrator: MCPOrchestrator = Depends(get_orchestrator)
):
    """获取所有已注册服务的详细信息"""
    services_info = []
    total_tools = 0
    
    # 获取所有服务的详细信息
    for name, config in orchestrator.mcp_config.load_config().get("mcpServers", {}).items():
        service_tools = registry.get_tools_for_service(name)
        total_tools += len(service_tools)
        
        transport_type = infer_transport_type(config)
        keep_alive = infer_keep_alive(config)
        
        # 获取服务的真实健康状态
        is_healthy = await orchestrator.is_service_healthy(name)
        status = "healthy" if is_healthy else "unhealthy"
        
        services_info.append(ServiceInfo(
            url=config.get("url", ""),  # 如果没有 URL，则为空字符串
            name=name,
            transport_type=transport_type,
            status=status,
            tool_count=len(service_tools),
            keep_alive=keep_alive,
            working_dir=config.get("working_dir"),
            env=config.get("env"),
            last_heartbeat=registry.get_last_heartbeat(name),
            command=config.get("command"),  # 添加命令信息
            args=config.get("args"),  # 添加参数列表
            package_name=config.get("package_name")  # 添加包名信息
        ))
        
    return ServicesResponse(
        services=services_info,
        total_services=len(services_info),
        total_tools=total_tools
    )

@router.get("/tools", response_model=ToolsResponse)
async def list_tools(
    agent_id: Optional[str] = None,
    client_id: Optional[str] = None,
    registry: ServiceRegistry = Depends(get_registry),
    orchestrator: MCPOrchestrator = Depends(get_orchestrator)
):
    """获取工具列表
    
    可以通过以下方式查询：
    1. 不传任何ID - 返回所有工具
    2. 传入agent_id - 返回该agent关联的所有client的工具
    3. 传入client_id - 返回该client的工具
    """
    try:
        tools_info = []
        
        # 加载配置
        client_configs = load_client_configs()
        agent_clients = load_agent_clients()
        
        if client_id:
            # 按client_id查询
            if client_id not in client_configs:
                raise HTTPException(status_code=404, detail=f"Client {client_id} not found")
            
            client_config = client_configs[client_id]
            service_names = list(client_config["mcpServers"].keys())
            
            # 获取这些服务的工具
            for service_name in service_names:
                tool_names = registry.get_tools_for_service(service_name)
                for tool_name in tool_names:
                    tool_info = registry._get_detailed_tool_info(tool_name)
                    if tool_info:
                        tools_info.append(ToolInfo(
                            name=tool_info["name"],
                            description=tool_info["description"],
                            service_name=service_name,
                            client_id=client_id,
                            inputSchema=tool_info.get("inputSchema")
                        ))
                    
        elif agent_id:
            # 按agent_id查询
            if agent_id not in agent_clients:
                raise HTTPException(status_code=404, detail=f"Agent {agent_id} not found")
                
            client_ids = agent_clients[agent_id]
            
            # 获取所有关联client的工具
            for client_id in client_ids:
                if client_id in client_configs:
                    client_config = client_configs[client_id]
                    service_names = list(client_config["mcpServers"].keys())
                    
                    for service_name in service_names:
                        tool_names = registry.get_tools_for_service(service_name)
                        for tool_name in tool_names:
                            tool_info = registry._get_detailed_tool_info(tool_name)
                            if tool_info:
                                tools_info.append(ToolInfo(
                                    name=tool_info["name"],
                                    description=tool_info["description"],
                                    service_name=service_name,
                                    client_id=client_id,
                                    inputSchema=tool_info.get("inputSchema")
                                ))
                            
        else:
            # 返回所有工具
            for tool in registry.get_all_tool_info():
                tools_info.append(ToolInfo(
                    name=tool["name"],
                    description=tool["description"],
                    service_name=tool.get("service_name"),
                    client_id=None,  # 全局工具没有关联的client_id
                    inputSchema=tool.get("inputSchema")
                ))
        
        return ToolsResponse(
            tools=tools_info,
            total_tools=len(tools_info)
        )
        
    except Exception as e:
        logger.error(f"Error listing tools: {e}")
        raise HTTPException(status_code=500, detail=str(e))

