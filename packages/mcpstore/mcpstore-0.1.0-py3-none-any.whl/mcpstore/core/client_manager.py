import os
import json
import random
import string
from datetime import datetime
from typing import Dict, Any, Optional, List
import logging

logger = logging.getLogger(__name__)

CLIENT_SERVICES_PATH = os.path.join(os.path.dirname(__file__), '../config/client_services.json')

class ClientManager:
    """管理客户端配置的类"""
    
    def __init__(self, services_path: Optional[str] = None):
        """
        初始化客户端管理器
        
        Args:
            services_path: 配置文件目录
        """
        self.services_path = services_path or CLIENT_SERVICES_PATH
        self._ensure_file()
        self.client_services = self.load_all_clients()
        self.main_client_id = "main_client"  # 主客户端ID
        
    def _ensure_file(self):
        if not os.path.exists(self.services_path):
            with open(self.services_path, 'w', encoding='utf-8') as f:
                json.dump({}, f)

    def load_all_clients(self) -> Dict[str, Any]:
        """加载所有客户端配置"""
        with open(self.services_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def save_all_clients(self, data: Dict[str, Any]):
        """保存所有客户端配置"""
        with open(self.services_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def get_client_config(self, client_id: str) -> Optional[Dict[str, Any]]:
        """获取客户端配置"""
        all_clients = self.load_all_clients()
        return all_clients.get(client_id)

    def save_client_config(self, client_id: str, config: Dict[str, Any]):
        """保存客户端配置"""
        all_clients = self.load_all_clients()
        all_clients[client_id] = config
        self.save_all_clients(all_clients)
        logger.info(f"Saved config for client_id={client_id}")

    def generate_client_id(self) -> str:
        """生成唯一的客户端ID"""
        ts = datetime.now().strftime("%Y%m%d%H%M%S")
        return f"client_{ts}"

    def create_client_config_from_names(self, service_names: List[str], mcp_config: Dict[str, Any]) -> Dict[str, Any]:
        """从服务名称列表生成新的客户端配置"""
        all_services = mcp_config.get("mcpServers", {})
        selected = {name: all_services[name] for name in service_names if name in all_services}
        return {"mcpServers": selected}

    def add_client(self, config: Dict[str, Any], client_id: Optional[str] = None) -> str:
        """
        添加新的客户端配置
        
        Args:
            config: 客户端配置
            client_id: 可选的客户端ID，如果不提供则自动生成
            
        Returns:
            使用的客户端ID
        """
        if not client_id:
            client_id = self.generate_client_id()
        self.client_services[client_id] = config
        self.save_client_config(client_id, config)
        return client_id
    
    def remove_client(self, client_id: str) -> bool:
        """
        移除客户端配置
        
        Args:
            client_id: 要移除的客户端ID
            
        Returns:
            是否成功移除
        """
        if client_id in self.client_services:
            del self.client_services[client_id]
            return self.save_client_config(client_id, {})
        return False
    
    def has_client(self, client_id: str) -> bool:
        """
        检查客户端是否存在
        
        Args:
            client_id: 客户端ID
            
        Returns:
            是否存在
        """
        return client_id in self.client_services
    
    def get_all_clients(self) -> Dict[str, Any]:
        """
        获取所有客户端配置
        
        Returns:
            所有客户端配置的字典
        """
        return self.client_services.copy() 
