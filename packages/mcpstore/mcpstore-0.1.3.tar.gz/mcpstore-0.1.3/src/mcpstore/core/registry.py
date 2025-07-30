import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import logging
from datetime import datetime
from typing import Dict, Any, Optional, Tuple, List, Set, TypeVar, Generic, Protocol

logger = logging.getLogger(__name__)

# 定义一个协议，表示任何具有call_tool方法的会话类型
class SessionProtocol(Protocol):
    async def call_tool(self, tool_name: str, tool_args: Dict[str, Any]) -> Any:
        ...

# 会话类型变量
SessionType = TypeVar('SessionType')

class ServiceRegistry:
    """Manages the state of connected services and their tools."""
    def __init__(self):
        self.sessions: Dict[str, Any] = {}  # service_name -> session
        self.service_health: Dict[str, datetime] = {} # service_name -> last_heartbeat_time
        self.tool_cache: Dict[str, Dict[str, Any]] = {} # tool_name -> tool_definition
        self.tool_to_session_map: Dict[str, Any] = {} # tool_name -> session
        logger.info("ServiceRegistry initialized.")

    def clear(self):
        """清空所有注册的服务和工具"""
        self.sessions.clear()
        self.service_health.clear()
        self.tool_cache.clear()
        self.tool_to_session_map.clear()

    def add_service(self, name: str, session: Any, tools: List[Tuple[str, Dict[str, Any]]]) -> List[str]:
        """Adds a new service, its session, and tools to the registry. Returns added tool names."""
        print(f"[DEBUG][add_service] name={name}, id(session)={id(session)}")
        if name in self.sessions:
            logger.warning(f"Attempting to add already registered service: {name}. Removing old service before overwriting.")
            self.remove_service(name)

        self.sessions[name] = session
        self.service_health[name] = datetime.now() # Mark healthy on add

        added_tool_names = []
        for tool_name, tool_definition in tools:
            # 检查工具名称是否属于当前服务
            if not tool_name.startswith(f"{name}_"):
                logger.warning(f"Tool '{tool_name}' does not belong to service '{name}'. Skipping this tool.")
                continue
                
            # 检查工具名称是否已存在
            if tool_name in self.tool_cache:
                # 如果工具已存在，检查是否属于同一个服务
                existing_session = self.tool_to_session_map.get(tool_name)
                if existing_session is not session:
                    logger.warning(f"Tool name conflict: '{tool_name}' from {name} conflicts with existing tool. Skipping this tool.")
                    continue
                    
            # 添加工具到缓存
            self.tool_cache[tool_name] = tool_definition
            self.tool_to_session_map[tool_name] = session
            added_tool_names.append(tool_name)
            
        logger.info(f"Service '{name}' added with tools: {added_tool_names}")
        return added_tool_names

    def remove_service(self, name: str) -> Optional[Any]:
        """Removes a service and its associated tools from the registry."""
        session = self.sessions.pop(name, None)
        
        if not session:
            logger.warning(f"Attempted to remove non-existent service: {name}")
            return None

        # Remove health record
        if name in self.service_health:
            del self.service_health[name]

        # Remove associated tools efficiently
        tools_to_remove = [tool_name for tool_name, owner_session in self.tool_to_session_map.items() if owner_session == session]
        if tools_to_remove:
            logger.info(f"Removing tools from registry associated with {name}: {tools_to_remove}")
            for tool_name in tools_to_remove:
                if tool_name in self.tool_cache: del self.tool_cache[tool_name]
                if tool_name in self.tool_to_session_map: del self.tool_to_session_map[tool_name]

        logger.info(f"Service '{name}' removed from registry.")
        return session

    def get_session(self, name: str) -> Optional[Any]:
        """Get session by service name"""
        return self.sessions.get(name)

    def get_session_for_tool(self, tool_name: str) -> Optional[Any]:
        """Get session by tool name"""
        return self.tool_to_session_map.get(tool_name)

    def get_all_tools(self) -> List[Dict[str, Any]]:
        """获取所有工具的定义"""
        all_tools = []
        
        # 遍历所有工具并添加服务信息
        for tool_name, tool_def in self.tool_cache.items():
            # 获取工具所属的服务信息
            session = self.tool_to_session_map.get(tool_name)
            service_name = None
            
            # 查找工具所属的服务
            for name, sess in self.sessions.items():
                if sess is session:
                    service_name = name
                    break
            
            # 创建包含服务信息的工具定义
            tool_with_service = tool_def.copy()
            
            # 如果是第一层级不包含function的情况，需要调整结构
            if "function" not in tool_with_service and isinstance(tool_with_service, dict):
                tool_with_service = {
                    "type": "function",
                    "function": tool_with_service
                }
            
            # 添加服务信息到函数名称或描述
            if "function" in tool_with_service:
                function_data = tool_with_service["function"]
                
                # 添加服务信息到描述中
                if service_name:
                    original_description = function_data.get("description", "")
                    if not original_description.endswith(f" (来自服务: {service_name})"):
                        function_data["description"] = f"{original_description} (来自服务: {service_name})"
                
                # 在内部保存服务信息，便于后续使用
                function_data["service_info"] = {
                    "service_name": service_name
                }
            
            all_tools.append(tool_with_service)
        
        logger.info(f"Returning {len(all_tools)} tools from {len(self.get_all_service_names())} services")
        return all_tools
        
    def get_all_tool_info(self) -> List[Dict[str, Any]]:
        """获取所有工具的详细信息"""
        tools_info = []
        for tool_name in self.tool_cache.keys():
            # 获取工具所属的服务
            session = self.tool_to_session_map.get(tool_name)
            service_name = None
            
            # 查找工具所属的服务名称
            for name, sess in self.sessions.items():
                if sess is session:
                    service_name = name
                    break
            
            # 获取详细工具信息
            detailed_tool = self._get_detailed_tool_info(tool_name)
            if detailed_tool:
                # 添加服务信息
                detailed_tool["service_name"] = service_name
                tools_info.append(detailed_tool)
            
        return tools_info
        
    def get_connected_services(self) -> List[Dict[str, Any]]:
        """获取所有已连接服务的信息"""
        services = []
        for name in self.get_all_service_names():
            tools = self.get_tools_for_service(name)
            services.append({
                "name": name,
                "tool_count": len(tools)
            })
        return services

    def get_tools_for_service(self, name: str) -> List[str]:
        """Get list of tools provided by the specified service"""
        session = self.sessions.get(name)
        logger.info(f"Getting tools for service: {name}")
        print(f"[DEBUG][get_tools_for_service] name={name}, id(session)={id(session) if session else None}")
        
        if not session:
            return []
            
        # 找到所有属于这个服务的工具（工具名以服务名为前缀）
        tools = [tool_name for tool_name in self.tool_cache.keys() if tool_name.startswith(f"{name}_")]
        
        return tools

    def _extract_description_from_schema(self, prop_info):
        """从 schema 中提取描述信息"""
        if isinstance(prop_info, dict):
            # 优先查找 description 字段
            if 'description' in prop_info:
                return prop_info['description']
            # 其次查找 title 字段
            elif 'title' in prop_info:
                return prop_info['title']
            # 检查是否有 anyOf 或 allOf 结构
            elif 'anyOf' in prop_info:
                for item in prop_info['anyOf']:
                    if isinstance(item, dict) and 'description' in item:
                        return item['description']
            elif 'allOf' in prop_info:
                for item in prop_info['allOf']:
                    if isinstance(item, dict) and 'description' in item:
                        return item['description']

        return "无描述"

    def _extract_type_from_schema(self, prop_info):
        """从 schema 中提取类型信息"""
        if isinstance(prop_info, dict):
            if 'type' in prop_info:
                return prop_info['type']
            elif 'anyOf' in prop_info:
                # 处理 Union 类型
                types = []
                for item in prop_info['anyOf']:
                    if isinstance(item, dict) and 'type' in item:
                        types.append(item['type'])
                return '|'.join(types) if types else '未知'
            elif 'allOf' in prop_info:
                # 处理 intersection 类型
                for item in prop_info['allOf']:
                    if isinstance(item, dict) and 'type' in item:
                        return item['type']

        return "未知"

    def _get_detailed_tool_info(self, tool_name: str) -> Dict[str, Any]:
        """获取工具的详细信息"""
        tool_def = self.tool_cache.get(tool_name)
        if not tool_def:
            return {}
            
        # 获取工具所属的服务
        session = self.tool_to_session_map.get(tool_name)
        service_name = None
        
        # 查找工具所属的服务
        if session:
            for name, sess in self.sessions.items():
                if sess is session:
                    service_name = name
                    break
                    
        # 提取工具信息
        if "function" in tool_def:
            function_data = tool_def["function"]
            tool_info = {
                "name": tool_name,
                "description": function_data.get("description", ""),
                "service_name": service_name,
                "inputSchema": function_data.get("parameters", {})
            }
        else:
            tool_info = {
                "name": tool_name,
                "description": tool_def.get("description", ""),
                "service_name": service_name,
                "inputSchema": tool_def.get("parameters", {})
            }
            
        return tool_info

    def get_service_details(self, name: str) -> Dict[str, Any]:
        """Get detailed information for the specified service"""
        if name not in self.sessions:
            return {}
            
        logger.info(f"Getting service details for: {name}")
        session = self.sessions.get(name)
        print(f"[DEBUG][get_service_details] name={name}, id(session)={id(session) if session else None}")
        tools = self.get_tools_for_service(name)
        last_heartbeat = self.service_health.get(name)
        
        # 获取详细工具信息
        detailed_tools = []
        for tool_name in tools:
            detailed_tool = self._get_detailed_tool_info(tool_name)
            if detailed_tool:
                detailed_tools.append(detailed_tool)
        
        return {
            "name": name,
            "tools": detailed_tools,
            "tool_count": len(tools),
            "last_heartbeat": str(last_heartbeat) if last_heartbeat else "N/A",
            "connected": name in self.sessions
        }

    def get_all_service_names(self) -> List[str]:
        """Get names of all active services"""
        return list(self.sessions.keys())

    def update_service_health(self, name: str):
        """Updates the last heartbeat time for a service."""
        if name in self.sessions:
            self.service_health[name] = datetime.now()
            logger.debug(f"Health updated for service: {name}")

    def get_last_heartbeat(self, name: str) -> Optional[datetime]:
        """Get last heartbeat time for a service"""
        return self.service_health.get(name)

    def has_service(self, name: str) -> bool:
        """Check if a service exists"""
        return name in self.sessions

    def get_service_config(self, name: str) -> Optional[Dict[str, Any]]:
        """获取服务配置"""
        if not self.has_service(name):
            return None
            
        # 从 orchestrator 的 mcp_config 获取配置
        from api.deps import app_state
        orchestrator = app_state.get("orchestrator")
        if orchestrator and orchestrator.mcp_config:
            return orchestrator.mcp_config.get_service_config(name)
            
        return None
