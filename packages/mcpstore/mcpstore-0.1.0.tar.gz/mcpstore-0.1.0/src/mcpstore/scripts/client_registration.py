import json
import logging
import os
import uuid
from datetime import datetime
from typing import List, Dict, Any, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from api.deps import get_orchestrator, get_registry
from core.orchestrator import MCPOrchestrator
from core.registry import ServiceRegistry
from mcpstore.core.client_manager import ClientManager

router = APIRouter()
logger = logging.getLogger(__name__)

class ClientRegistrationRequest(BaseModel):
    """客户端注册请求"""
    agent_id: Optional[str] = None  # 可选的agent_id
    service_names: List[str]

class ServiceRegistrationStatus(BaseModel):
    """服务注册状态"""
    status: str  # success 或 failed
    message: Optional[str] = None
    error: Optional[str] = None

class ClientRegistrationResponse(BaseModel):
    """客户端注册响应"""
    agent_id: str  # 返回传入的或新生成的agent_id
    clients: Dict[str, Dict[str, Any]]  # client_id -> client_config
    services_status: Dict[str, ServiceRegistrationStatus]  # service_name -> status
    total_success: int
    total_failed: int
    status: str = "success"
    message: Optional[str] = None

def generate_agent_id() -> str:
    """生成agent_id"""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    random_suffix = str(uuid.uuid4())[:8]
    return f"agent_{timestamp}_{random_suffix}"

def generate_client_id(agent_id: str, index: int) -> str:
    """根据agent_id生成client_id"""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"{agent_id}_client_{index}_{timestamp}"

def save_client_configs(configs: Dict[str, Any]):
    """保存客户端配置到文件"""
    config_dir = "configs"
    os.makedirs(config_dir, exist_ok=True)
    
    # 保存client_services.json
    client_services_path = os.path.join(config_dir, "client_services.json")
    with open(client_services_path, "w") as f:
        json.dump(configs, f, indent=2)

def save_agent_clients(agent_id: str, client_ids: List[str]):
    """保存agent和client的关系到文件"""
    config_dir = "configs"
    agent_clients_path = os.path.join(config_dir, "agent_clients.json")
    
    # 读取现有配置
    agent_clients = {}
    if os.path.exists(agent_clients_path):
        with open(agent_clients_path, "r") as f:
            agent_clients = json.load(f)
    
    # 更新配置
    agent_clients[agent_id] = client_ids
    
    # 保存配置
    with open(agent_clients_path, "w") as f:
        json.dump(agent_clients, f, indent=2)

def load_client_configs() -> Dict[str, Any]:
    """加载客户端配置"""
    config_dir = "configs"
    client_services_path = os.path.join(config_dir, "client_services.json")
    
    if os.path.exists(client_services_path):
        with open(client_services_path, "r") as f:
            return json.load(f)
    return {}

def load_agent_clients() -> Dict[str, List[str]]:
    """加载agent和client的关系"""
    config_dir = "configs"
    agent_clients_path = os.path.join(config_dir, "agent_clients.json")
    
    if os.path.exists(agent_clients_path):
        with open(agent_clients_path, "r") as f:
            return json.load(f)
    return {}

@router.post("/register_clients", response_model=ClientRegistrationResponse)
async def register_clients(
    request: ClientRegistrationRequest,
    orchestrator: MCPOrchestrator = Depends(get_orchestrator),
    registry: ServiceRegistry = Depends(get_registry)
):
    """注册客户端
    
    为agent创建多个client，每个client对应一个服务。
    如果没有提供agent_id，会自动生成一个。
    """
    try:
        # 如果没有提供agent_id，生成一个
        agent_id = request.agent_id or generate_agent_id()
        
        # 生成client配置
        client_configs = {}
        client_ids = []
        services_status = {}
        total_success = 0
        total_failed = 0
        
        for i, service_name in enumerate(request.service_names):
            try:
                # 验证服务是否存在
                service_config = registry.get_service_config(service_name)
                if not service_config:
                    raise Exception(f"Service {service_name} not found")
                
                # 生成client_id并创建配置
                client_id = generate_client_id(agent_id, i)
                client_ids.append(client_id)
                
                client_configs[client_id] = {
                    "mcpServers": {
                        service_name: service_config
                    }
                }
                
                # 记录成功状态
                services_status[service_name] = ServiceRegistrationStatus(
                    status="success",
                    message=f"Successfully registered with client {client_id}"
                )
                total_success += 1
                
            except Exception as e:
                # 记录失败状态
                services_status[service_name] = ServiceRegistrationStatus(
                    status="failed",
                    error=str(e)
                )
                total_failed += 1
                logger.error(f"Failed to register service {service_name}: {e}")
        
        if client_configs:  # 如果至少有一个服务注册成功
            # 保存配置
            save_client_configs(client_configs)
            save_agent_clients(agent_id, client_ids)
            
            # 创建会话
            session = orchestrator.session_manager.create_session(agent_id)
            
            return ClientRegistrationResponse(
                agent_id=agent_id,
                clients=client_configs,
                services_status=services_status,
                total_success=total_success,
                total_failed=total_failed,
                status="success",
                message=f"Successfully registered {total_success} clients, {total_failed} failed"
            )
        else:
            raise HTTPException(
                status_code=500,
                detail="All service registrations failed"
            )
            
    except Exception as e:
        logger.error(f"Failed to register clients: {e}")
        raise HTTPException(status_code=500, detail=str(e)) 
