from typing import Dict, Any
from mcpstore.core.orchestrator import MCPOrchestrator
from mcpstore.core.registry import ServiceRegistry
from fastapi import HTTPException

# 全局应用状态
app_state: Dict[str, Any] = {}

def get_orchestrator() -> MCPOrchestrator:
    orchestrator = app_state.get("orchestrator")
    if orchestrator is None:
        raise HTTPException(status_code=503, detail="Service not ready (Orchestrator not initialized)")
    return orchestrator

def get_registry() -> ServiceRegistry:
    registry = app_state.get("registry")
    if registry is None:
        raise HTTPException(status_code=503, detail="Service not ready (Registry not initialized)")
    return registry
