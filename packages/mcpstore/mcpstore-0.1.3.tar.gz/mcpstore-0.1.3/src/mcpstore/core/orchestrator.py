import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

"""
MCP服务编排器

该模块提供了MCPOrchestrator类，用于管理MCP服务的连接、工具调用和查询处理。
它是FastAPI应用程序的核心组件，负责协调客户端和服务之间的交互。
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional, Tuple, Set, Union, AsyncGenerator
from datetime import datetime, timedelta
from urllib.parse import urljoin

from mcpstore.core.registry import ServiceRegistry
from mcpstore.core.client_manager import ClientManager
from fastmcp import Client
from fastmcp.client.transports import (
    MCPConfigTransport,
    StreamableHttpTransport,
    SSETransport,
    PythonStdioTransport,
    NodeStdioTransport,
    UvxStdioTransport,
    NpxStdioTransport
)
from mcpstore.plugins.json_mcp import MCPConfig
from mcpstore.scripts.models import TransportType, ServiceRegistrationResult
from mcpstore.core.session_manager import SessionManager

logger = logging.getLogger(__name__)

class MCPOrchestrator:
    """
    MCP服务编排器
    
    负责管理服务连接、工具调用和查询处理。
    """
    
    def __init__(self, config: Dict[str, Any], registry: ServiceRegistry):
        """
        初始化MCP编排器
        
        Args:
            config: 配置字典
            registry: 服务注册表实例
        """
        self.config = config
        self.registry = registry
        self.clients: Dict[str, Client] = {}  # key为mcpServers的服务名
        self.main_client: Optional[Client] = None
        self.main_client_ctx = None  # async context manager for main_client
        self.main_config = {"mcpServers": {}}  # 中央配置
        self.agent_clients: Dict[str, Client] = {}  # agent_id -> client映射
        self.pending_reconnection: Set[str] = set()
        self.react_agent = None
        
        # 从配置中获取心跳和重连设置
        timing_config = config.get("timing", {})
        self.heartbeat_interval = timedelta(seconds=int(timing_config.get("heartbeat_interval_seconds", 60)))
        self.heartbeat_timeout = timedelta(seconds=int(timing_config.get("heartbeat_timeout_seconds", 180)))
        self.reconnection_interval = timedelta(seconds=int(timing_config.get("reconnection_interval_seconds", 60)))
        self.http_timeout = int(timing_config.get("http_timeout_seconds", 10))
        
        # 监控任务
        self.heartbeat_task = None
        self.reconnection_task = None
        self.mcp_config = MCPConfig()
        
        # 客户端管理器
        self.client_manager = ClientManager()
        
        # 会话管理器
        self.session_manager = SessionManager()
    
    async def setup(self):
        """初始化编排器资源（不再做服务注册）"""
        logger.info("Setting up MCP Orchestrator...")
        # 只做必要的资源初始化
        pass
    
    async def start_monitoring(self):
        """启动后台健康检查和重连监视器"""
        logger.info("Starting monitoring tasks...")
        
        # 启动心跳监视器
        if self.heartbeat_task is None or self.heartbeat_task.done():
            logger.info(f"Starting heartbeat monitor. Interval: {self.heartbeat_interval.total_seconds()}s")
            self.heartbeat_task = asyncio.create_task(self._heartbeat_loop())
        
        # 启动重连监视器
        if self.reconnection_task is None or self.reconnection_task.done():
            logger.info(f"Starting reconnection monitor. Interval: {self.reconnection_interval.total_seconds()}s")
            self.reconnection_task = asyncio.create_task(self._reconnection_loop())
    
    async def _heartbeat_loop(self):
        """后台循环，用于定期健康检查"""
        while True:
            await asyncio.sleep(self.heartbeat_interval.total_seconds())
            await self._check_services_health()
    
    async def _check_services_health(self):
        """检查所有服务的健康状态"""
        logger.debug("Running periodic health check for all services...")
        for name in self.clients:
            try:
                is_healthy = await self.is_service_healthy(name)
                if is_healthy:
                    logger.debug(f"Health check SUCCESS for: {name}")
                    self.registry.update_service_health(name)
                else:
                    logger.warning(f"Health check FAILED for {name}")
                    self.pending_reconnection.add(name)
            except Exception as e:
                logger.warning(f"Health check error for {name}: {e}")
                self.pending_reconnection.add(name)
    
    async def _reconnection_loop(self):
        """定期尝试重新连接服务的后台循环"""
        while True:
            await asyncio.sleep(self.reconnection_interval.total_seconds())
            await self._attempt_reconnections()
    
    async def _attempt_reconnections(self):
        """尝试重新连接所有待重连的服务"""
        if not self.pending_reconnection:
            return  # 如果没有待重连的服务，跳过
        
        # 创建副本以避免迭代过程中修改集合的问题
        names_to_retry = list(self.pending_reconnection)
        logger.info(f"Attempting to reconnect {len(names_to_retry)} service(s): {names_to_retry}")
        
        for name in names_to_retry:
            try:
                # 尝试重新连接
                success, message = await self.connect_service(name)
                if success:
                    logger.info(f"Reconnection successful for: {name}")
                    self.pending_reconnection.discard(name)
                else:
                    logger.warning(f"Reconnection attempt failed for {name}: {message}")
                    # 保持name在pending_reconnection中，等待下一个周期
            except Exception as e:
                logger.warning(f"Reconnection attempt failed for {name}: {e}")
    
    async def connect_service(self, name: str, url: str = None) -> Tuple[bool, str]:
        """
        连接到指定的服务
        
        Args:
            name: 服务名称
            url: 服务URL（可选，如果不提供则从配置中获取）
            
        Returns:
            Tuple[bool, str]: (是否成功, 消息)
        """
        try:
            # 获取服务配置
            service_config = self.mcp_config.get_service_config(name)
            if not service_config:
                return False, f"Service configuration not found for {name}"
                
            # 如果提供了URL，更新配置
            if url:
                service_config["url"] = url
                
            # 创建新的客户端
            client = Client({"mcpServers": {name: service_config}})
            
            # 尝试连接
            try:
                await client.list_tools()
                self.clients[name] = client
                logger.info(f"Service {name} connected successfully")
                return True, "Connected successfully"
            except Exception as e:
                logger.error(f"Failed to connect to service {name}: {e}")
                return False, str(e)
                
        except Exception as e:
            logger.error(f"Failed to connect service {name}: {e}")
            return False, str(e)
    
    async def disconnect_service(self, url_or_name: str) -> bool:
        """从配置中移除服务并更新main_client"""
        logger.info(f"Removing service: {url_or_name}")
        
        # 查找要移除的服务名
        name_to_remove = None
        for name, server in self.main_config.get("mcpServers", {}).items():
            if name == url_or_name or server.get("url") == url_or_name:
                name_to_remove = name
                break
                
        if name_to_remove:
            # 从main_config中移除
            if name_to_remove in self.main_config["mcpServers"]:
                del self.main_config["mcpServers"][name_to_remove]
                
            # 从配置文件中移除
            ok = self.mcp_config.remove_service(name_to_remove)
            if not ok:
                logger.warning(f"Failed to remove service {name_to_remove} from configuration file")
                
            # 从registry中移除
            self.registry.remove_service(name_to_remove)
                
            # 重新创建main_client
            if self.main_config.get("mcpServers"):
                self.main_client = Client(self.main_config)
                
                # 更新所有agent_clients
                for agent_id in list(self.agent_clients.keys()):
                    self.agent_clients[agent_id] = Client(self.main_config)
                    logger.info(f"Updated client for agent {agent_id} after removing service")
                
            else:
                # 如果没有服务了，清除main_client
                self.main_client = None
                # 清除所有agent_clients
                self.agent_clients.clear()
                
            return True
        else:
            logger.warning(f"Service {url_or_name} not found in configuration.")
            return False
    
    async def refresh_services(self):
        """手动刷新所有服务连接（重新加载mcp.json）"""
        await self.load_from_config()
    
    async def is_service_healthy(self, name: str) -> bool:
        """
        检查服务是否健康
        
        Args:
            name: 服务名
            
        Returns:
            bool: 服务是否健康
        """
        try:
            # 获取服务配置
            service_config = self.mcp_config.get_service_config(name)
            if not service_config:
                logger.warning(f"Service configuration not found for {name}")
                return False
            print(f'此时的name是{name},service_config是{service_config}')
            # 创建新的客户端并在上下文管理器中使用 ping 方法
            client = Client({"mcpServers": {name: service_config}})
            try:
                async with client as session:
                    await session.ping()
                    return True
            except Exception as e:
                logger.warning(f"Health check failed for {name}: {e}")
                return False
        except Exception as e:
            logger.warning(f"Health check failed for {name}: {e}")
            return False
    
    # async def process_unified_query(
    #     self,
    #     query: str,
    #     agent_id: Optional[str] = None,
    #     mode: str = "react",
    #     include_trace: bool = False
    # ) -> Union[str, Dict[str, Any]]:
    #     """处理统一查询"""
    #     # 获取或创建会话
    #     session = self.session_manager.get_or_create_session(agent_id)
    #
    #     if not session.tools:
    #         # 如果会话没有工具，加载所有可用工具
    #         for service_name, client in self.clients.items():
    #             try:
    #                 tools = await client.list_tools()
    #                 for tool in tools:
    #                     session.add_tool(tool.name, {
    #                         "name": tool.name,
    #                         "description": tool.description,
    #                         "inputSchema": tool.inputSchema if hasattr(tool, "inputSchema") else None
    #                     }, service_name)
    #                     session.add_service(service_name, client)
    #             except Exception as e:
    #                 logger.error(f"Failed to load tools from service {service_name}: {e}")
    #
    #     # 处理查询...
    #     return {"result": "query processed", "session_id": session.agent_id}
    
    async def execute_tool(
        self,
        service_name: str,
        tool_name: str,
        parameters: Dict[str, Any],
        agent_id: Optional[str] = None
    ) -> Any:
        """执行工具"""
        if agent_id:
            # 如果提供了agent_id，从会话中获取client
            session = self.session_manager.get_session(agent_id)
            if session:
                client = session.services.get(service_name)
                if not client:
                    raise Exception(f"Service {service_name} not found in session")
            else:
                raise Exception(f"Session not found for agent {agent_id}")
        else:
            # 否则使用默认client
            client = self.clients.get(service_name)
            if not client:
                raise Exception(f"Service {service_name} not found")
        
        try:
            async with client:
                result = await client.call_tool(tool_name, parameters)
                logger.info(f"Tool {tool_name} executed successfully")
                return result
        except Exception as e:
            logger.error(f"Failed to execute tool {tool_name}: {e}")
            raise Exception(f"Tool execution failed: {str(e)}")
    
    async def cleanup(self):
        """清理资源"""
        logger.info("Cleaning up MCP Orchestrator resources...")
        
        # 清理会话
        self.session_manager.cleanup_expired_sessions()
        
        # 停止监控任务
        if self.heartbeat_task and not self.heartbeat_task.done():
            self.heartbeat_task.cancel()
            try:
                await self.heartbeat_task
            except asyncio.CancelledError:
                pass
                
        if self.reconnection_task and not self.reconnection_task.done():
            self.reconnection_task.cancel()
            try:
                await self.reconnection_task
            except asyncio.CancelledError:
                pass
                
        # 关闭所有客户端连接
        for name, client in self.clients.items():
            try:
                await client.close()
            except Exception as e:
                logger.error(f"Error closing client {name}: {e}")
                
        self.clients.clear()
        self.pending_reconnection.clear()
        
    async def register_agent_client(self, agent_id: str, config: Optional[Dict[str, Any]] = None) -> Client:
        """
        为agent注册一个新的client实例
        
        Args:
            agent_id: 代理ID
            config: 可选的配置，如果为None则使用main_config
            
        Returns:
            新创建的Client实例
        """
        # 使用main_config或提供的config创建新的client
        agent_config = config or self.main_config
        agent_client = Client(agent_config)
        
        # 存储agent_client
        self.agent_clients[agent_id] = agent_client
        logger.info(f"Registered agent client for {agent_id}")
        
        return agent_client

    def get_agent_client(self, agent_id: str) -> Optional[Client]:
        """
        获取agent的client实例
        
        Args:
            agent_id: 代理ID
            
        Returns:
            Client实例或None
        """
        return self.agent_clients.get(agent_id)

    async def start_main_client(self, config: Dict[str, Any]):
        """启动 main_client 的 async with 生命周期，注册服务和工具"""
        self.main_client = Client(config)
        self.main_client_ctx = self.main_client.__aenter__()
        try:
            await self.main_client_ctx
            logger.info(f"main_client connected: {self.main_client.is_connected()}")
            logger.info(f"main_client transport: {self.main_client.transport}")
            logger.info(f"main_client session: {getattr(self.main_client, 'session', None)}")
            try:
                tool_list = await self.main_client.list_tools()
                all_tools = []
                for tool in tool_list:
                    # 正确处理FastMCP的Tool对象
                    tool_name = tool.name
                    tool_def = {
                        "type": "function",
                        "function": {
                            "name": tool_name,
                            "description": tool.description,
                            "parameters": {
                                "type": "object",
                                "properties": {},
                                "required": []
                            }
                        }
                    }
                    
                    # 处理参数信息
                    if hasattr(tool, 'inputSchema') and tool.inputSchema:
                        schema = tool.inputSchema
                        if isinstance(schema, dict):
                            tool_def["function"]["parameters"] = schema
                        
                    all_tools.append((tool_name, tool_def))
                    
                logger.info(f"Retrieved {len(all_tools)} tools from main_client")
            except Exception as e:
                logger.warning(f"Failed to get tools from main_client: {e}")
                all_tools = []
            
            self.clients.clear()
            self.registry.clear()
            for name, service_config in config.get("mcpServers", {}).items():
                try:
                    self.clients[name] = self.main_client
                    self.registry.add_service(name, self.main_client, all_tools, name)
                except Exception as e:
                    logger.error(f"Failed to register service {name}: {e}")
        except Exception as e:
            logger.error(f"main_client MCP服务连接失败: {e}")
            raise

    async def stop_main_client(self):
        """优雅关闭 main_client 的 async with 生命周期"""
        if self.main_client and self.main_client_ctx:
            try:
                await self.main_client.__aexit__(None, None, None)
                logger.info("main_client closed.")
            except Exception as e:
                logger.error(f"Error closing main_client: {e}")
        self.main_client = None
        self.main_client_ctx = None

    async def agent_client_context(self, config: Dict[str, Any]):
        """agent client 的 async with 临时上下文管理器"""
        client = Client(config)
        try:
            async with client:
                logger.info(f"agent_client connected: {client.is_connected()}")
                logger.info(f"agent_client transport: {client.transport}")
                logger.info(f"agent_client session: {getattr(client, 'session', None)}")
                yield client
        except Exception as e:
            logger.error(f"agent_client 连接或操作失败: {e}")
            raise

    async def register_json_services(self, config: Dict[str, Any], client_id: Optional[str] = None) -> Dict[str, Any]:
        """注册JSON配置中的服务"""
        try:
            # 创建客户端
            client = Client(config)
            
            # 获取工具列表
            try:
                # 获取所有服务名称
                service_names = list(config.get("mcpServers", {}).keys())
                if not service_names:
                    logger.warning("No services found in configuration")
                    return {
                        "client_id": client_id or "main_client",
                        "services": {},
                        "total_success": 0,
                        "total_failed": 0
                    }
                
                async with client:    
                    # 获取工具列表
                    tool_list = await client.list_tools()
                    if not tool_list:
                        logger.warning("No tools found")
                        return {
                            "client_id": client_id or "main_client",
                            "services": {},
                            "total_success": 0,
                            "total_failed": 0
                        }
                        
                    # 处理工具列表
                    all_tools = []
                    for tool in tool_list:
                        # 正确处理FastMCP的Tool对象
                        tool_name = tool.name
                        
                        # 根据工具名前缀确定所属服务
                        service_name = None
                        for name in service_names:
                            if tool_name.startswith(f"{name}_"):
                                service_name = name
                                break
                                
                        if not service_name:
                            logger.warning(f"Tool {tool_name} does not belong to any service, skipping")
                            continue
                            
                        # 处理参数信息
                        parameters = {}
                        if hasattr(tool, 'inputSchema') and tool.inputSchema:
                            parameters = tool.inputSchema
                        elif hasattr(tool, 'parameters') and tool.parameters:
                            parameters = tool.parameters
                            
                        tool_def = {
                            "type": "function",
                            "function": {
                                "name": tool_name,
                                "description": tool.description,
                                "parameters": parameters
                            }
                        }
                        all_tools.append((tool_name, tool_def))
                    
                    # 为每个服务注册其工具
                    for service_name in service_names:
                        # 过滤出属于当前服务的工具
                        service_tools = [(name, tool_def) for name, tool_def in all_tools if name.startswith(f"{service_name}_")]
                        logger.info(f"Filtered {len(service_tools)} tools for service {service_name}")
                        
                        # 注册服务及其工具
                        self.registry.add_service(service_name, client, service_tools)
                        
                        # 保存客户端实例
                        self.clients[service_name] = client
                        
                    return {
                        "client_id": client_id or "main_client",
                        "services": {
                            name: {"status": "success", "message": "Service registered successfully"}
                            for name in service_names
                        },
                        "total_success": len(service_names),
                        "total_failed": 0
                    }
            except Exception as e:
                logger.error(f"Error retrieving tools: {e}", exc_info=True)
                return {
                    "client_id": client_id or "main_client",
                    "services": {},
                    "total_success": 0,
                    "total_failed": 1,
                    "error": str(e)
                }
        except Exception as e:
            logger.error(f"Error registering services: {e}", exc_info=True)
            return {
                "client_id": client_id or "main_client",
                "services": {},
                "total_success": 0,
                "total_failed": 1,
                "error": str(e)
            }

    def create_client_config_from_names(self, service_names: list) -> Dict[str, Any]:
        """
        根据服务名列表，从 mcp.json 生成新的 client config
        """
        all_services = self.mcp_config.load_config().get("mcpServers", {})
        selected = {name: all_services[name] for name in service_names if name in all_services}
        return {"mcpServers": selected} 
