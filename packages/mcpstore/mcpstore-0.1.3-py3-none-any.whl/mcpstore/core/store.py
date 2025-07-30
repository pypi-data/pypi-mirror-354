from mcpstore.core.orchestrator import MCPOrchestrator
from mcpstore.core.registry import ServiceRegistry
from mcpstore.plugins.json_mcp import MCPConfig
from mcpstore.core.client_manager import ClientManager
from mcpstore.core.session_manager import SessionManager
from mcpstore.scripts.models import (
    RegisterRequestUnion, JsonRegistrationResponse, JsonUpdateRequest, JsonConfigResponse,
    ToolExecutionResponse, ClientRegistrationResponse
)
import logging
from typing import Optional, List, Dict, Any

class McpStore:
    def __init__(self, orchestrator: MCPOrchestrator, config: MCPConfig):
        self.orchestrator = orchestrator
        self.config = config
        self.registry = orchestrator.registry
        self.client_manager = orchestrator.client_manager
        self.session_manager = orchestrator.session_manager
        self.logger = logging.getLogger(__name__)

    async def register_service(self, payload: RegisterRequestUnion, agent_id: Optional[str] = None) -> Dict[str, str]:
        """注册服务，等价于 /register"""
        return await self.orchestrator._process_registration(payload, self.orchestrator, agent_id)

    async def register_json_service(self, client_id: Optional[str] = None, service_names: Optional[List[str]] = None) -> JsonRegistrationResponse:
        """批量注册服务，等价于 /register/json"""
        if client_id == self.client_manager.main_client_id or not client_id:
            config = self.config.load_config()
        else:
            if not service_names:
                raise ValueError("service_names required for non-main_client registration")
            config = self.orchestrator.create_client_config_from_names(service_names)
        results = await self.orchestrator.register_json_services(config, client_id=client_id)
        return JsonRegistrationResponse(
            client_id=results["client_id"],
            services={},
            total_success=results["total_services"],
            total_failed=0 if results["status"] == "success" else 1
        )

    async def update_json_service(self, payload: JsonUpdateRequest) -> JsonRegistrationResponse:
        """更新服务配置，等价于 PUT /register/json"""
        results = await self.orchestrator.register_json_services(
            config=payload.config,
            client_id=payload.client_id
        )
        return JsonRegistrationResponse(
            client_id=results["client_id"],
            services={
                name: result for name, result in results["services"].items()
            },
            total_success=results.get("total_success", 0),
            total_failed=results.get("total_failed", 0)
        )

    def get_json_config(self, client_id: Optional[str] = None) -> JsonConfigResponse:
        """查询服务配置，等价于 GET /register/json"""
        if not client_id or client_id == self.client_manager.main_client_id:
            config = self.config.load_config()
            return JsonConfigResponse(
                client_id=self.client_manager.main_client_id,
                config=config
            )
        else:
            config = self.client_manager.get_client_config(client_id)
            if not config:
                raise ValueError(f"Client configuration not found: {client_id}")
            return JsonConfigResponse(
                client_id=client_id,
                config=config
            )

    async def execute_tool(self, service_name: str, tool_name: str, parameters: Dict[str, Any], agent_id: Optional[str] = None) -> ToolExecutionResponse:
        """调用工具，等价于 /execute"""
        return await self.orchestrator.execute_tool(service_name, tool_name, parameters, agent_id)

    def register_clients(self, client_configs: Dict[str, Any]) -> ClientRegistrationResponse:
        """注册客户端，等价于 /register_clients"""
        # 这里只是示例，具体实现需根据 client_manager 逻辑完善
        for client_id, config in client_configs.items():
            self.client_manager.save_client_config(client_id, config)
        return ClientRegistrationResponse(status="success", client_ids=list(client_configs.keys()))

    async def get_health_status(self) -> Dict[str, Any]:
        """获取服务健康状态，等价于 /health"""
        services = []
        for name, config in self.config.load_config().get("mcpServers", {}).items():
            is_healthy = await self.orchestrator.is_service_healthy(name)
            service_status = {
                "name": name,
                "url": config.get("url", ""),
                "transport_type": config.get("transport", ""),
                "status": "healthy" if is_healthy else "unhealthy",
                "command": config.get("command"),
                "args": config.get("args"),
                "package_name": config.get("package_name")
            }
            services.append(service_status)
        return {
            "orchestrator_status": "running",
            "active_services": len(self.registry.sessions),
            "total_tools": len(self.registry.tool_cache),
            "services": services
        }

    def get_service_info(self, name: str) -> Dict[str, Any]:
        """获取指定服务信息，等价于 /service_info"""
        return self.registry.get_service_details(name)

    def list_services(self) -> List[str]:
        """获取所有服务列表，等价于 /services"""
        return self.registry.get_all_service_names()

    def list_tools(self) -> List[Dict[str, Any]]:
        """获取所有工具列表，等价于 /tools"""
        return self.registry.get_all_tool_info() 
