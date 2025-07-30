import logging
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.exception_handlers import validation_exception_handler

from mcpstore.scripts.service_management import router as service_router
from api.tool_execution import router as tool_execution_router
from api.client_registration import router as client_registration_router
from api.deps import app_state
from plugins.json_mcp import MCPConfig
from core.registry import ServiceRegistry
from core.orchestrator import MCPOrchestrator

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.StreamHandler(sys.stdout), logging.FileHandler("mcp_service.log")])
logger = logging.getLogger(__name__)

async def lifespan(app: FastAPI):
    logger.info("Application startup: Initializing components...")
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "plugins", "mcp.json")
    mcp_config_handler = MCPConfig(config_path)
    config = mcp_config_handler.load_config()
    registry = ServiceRegistry()
    orchestrator = MCPOrchestrator(config=config, registry=registry)
    await orchestrator.setup()
    await orchestrator.start_monitoring()
    logger.info("Registering main_client from mcp.json via unified logic...")
    await orchestrator.register_json_services(config, client_id="main_client")
    app_state["orchestrator"] = orchestrator
    app_state["registry"] = registry
    app_state["mcp_config"] = mcp_config_handler
    logger.info("Components initialized and background tasks started.")
    try:
        yield
    finally:
        logger.info("Application shutdown: Cleaning up resources...")
        orch = app_state.get("orchestrator")
        if orch:
            await orch.stop_main_client()
            await orch.cleanup()
        app_state.clear()
        logger.info("Application shutdown complete.")

app = FastAPI(lifespan=lifespan)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册API路由
# app.include_router(llm_agent_router)
app.include_router(service_router)
app.include_router(tool_execution_router)
app.include_router(client_registration_router)

# 注册异常处理
from fastapi.exceptions import RequestValidationError
app.add_exception_handler(RequestValidationError, validation_exception_handler) 
