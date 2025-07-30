"""
Main FastAPI application for Nivora AI SDK.
"""

import os
import asyncio
from contextlib import asynccontextmanager
from typing import Dict, Any

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from ..core.blockchain import BlockchainManager, NetworkConfig, NetworkType
from ..core.deployment import DeploymentManager
from ..core.monetization import MonetizationManager
from ..core.interoperability import CrossChainManager
from ..database.models import init_db
from ..utils.config import Config
from ..utils.logger import get_logger
from ..utils.exceptions import NivoraAIException

from .routes import agents, deployment, monitoring, monetization
from .websocket import websocket_endpoint, websocket_manager

logger = get_logger(__name__)

# Global managers
blockchain_manager: BlockchainManager = None
deployment_manager: DeploymentManager = None
monetization_manager: MonetizationManager = None
cross_chain_manager: CrossChainManager = None
config: Config = None

# Security
security = HTTPBearer(auto_error=False)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    global blockchain_manager, deployment_manager, monetization_manager, cross_chain_manager, config
    
    logger.info("Starting Nivora AI API...")
    
    try:
        # Initialize configuration
        config = Config()
        
        # Initialize database
        await init_db()
        
        # Initialize blockchain manager
        blockchain_manager = BlockchainManager()
        
        # Setup default networks
        await setup_default_networks()
        
        # Initialize other managers
        deployment_manager = DeploymentManager()
        monetization_manager = MonetizationManager()
        cross_chain_manager = CrossChainManager()
        
        # Start background tasks
        asyncio.create_task(periodic_health_check())
        
        logger.info("Nivora AI API started successfully")
        
        yield
        
    except Exception as e:
        logger.error(f"Failed to start Nivora AI API: {e}")
        raise
    
    finally:
        logger.info("Shutting down Nivora AI API...")
        
        # Cleanup resources
        if blockchain_manager:
            await blockchain_manager.disconnect_all_networks()
        
        # Close WebSocket connections
        await websocket_manager.disconnect_all()
        
        logger.info("Nivora AI API shutdown complete")


async def setup_default_networks():
    """Setup default blockchain networks."""
    try:
        # Ethereum Mainnet
        ethereum_config = NetworkConfig(
            network_type=NetworkType.ETHEREUM,
            rpc_url=os.getenv("ETHEREUM_RPC_URL", ""),
            chain_id=1,
            private_key=os.getenv("ETHEREUM_PRIVATE_KEY")
        )
        await blockchain_manager.add_network("ethereum", ethereum_config)
        
        # Polygon Mainnet
        polygon_config = NetworkConfig(
            network_type=NetworkType.POLYGON,
            rpc_url=os.getenv("POLYGON_RPC_URL", ""),
            chain_id=137,
            private_key=os.getenv("POLYGON_PRIVATE_KEY")
        )
        await blockchain_manager.add_network("polygon", polygon_config)
        
        # BSC Mainnet
        bsc_config = NetworkConfig(
            network_type=NetworkType.BSC,
            rpc_url=os.getenv("BSC_RPC_URL", ""),
            chain_id=56,
            private_key=os.getenv("BSC_PRIVATE_KEY")
        )
        await blockchain_manager.add_network("bsc", bsc_config)
        
        # Solana Mainnet
        solana_config = NetworkConfig(
            network_type=NetworkType.SOLANA,
            rpc_url=os.getenv("SOLANA_RPC_URL", ""),
            chain_id=101,
            private_key=os.getenv("SOLANA_PRIVATE_KEY")
        )
        await blockchain_manager.add_network("solana", solana_config)
        
        logger.info("Default networks configured")
        
    except Exception as e:
        logger.error(f"Failed to setup default networks: {e}")


async def periodic_health_check():
    """Periodic health check for blockchain networks."""
    while True:
        try:
            await asyncio.sleep(60)  # Check every minute
            
            network_status = await blockchain_manager.get_all_network_status()
            
            for network_name, status in network_status.items():
                if "error" in status:
                    logger.warning(f"Network {network_name} health check failed: {status['error']}")
                
        except Exception as e:
            logger.error(f"Health check error: {e}")


def get_config() -> Config:
    """Get configuration dependency."""
    return config


def get_blockchain_manager() -> BlockchainManager:
    """Get blockchain manager dependency."""
    return blockchain_manager


def get_deployment_manager() -> DeploymentManager:
    """Get deployment manager dependency."""
    return deployment_manager


def get_monetization_manager() -> MonetizationManager:
    """Get monetization manager dependency."""
    return monetization_manager


def get_cross_chain_manager() -> CrossChainManager:
    """Get cross-chain manager dependency."""
    return cross_chain_manager


async def verify_api_key(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """Verify API key."""
    if not credentials:
        raise HTTPException(status_code=401, detail="API key required")
    
    # In production, verify against database or external service
    api_key = credentials.credentials
    valid_api_keys = os.getenv("NIVORA_API_KEYS", "demo-key").split(",")
    
    if api_key not in valid_api_keys:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    return api_key


# Create FastAPI application
app = FastAPI(
    title="Nivora AI SDK API",
    description="Deploy, scale, and monetize AI agents across multiple blockchain networks",
    version="0.1.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure properly in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Exception handlers
@app.exception_handler(NivoraAIException)
async def nivora_exception_handler(request, exc: NivoraAIException):
    """Handle Nivora AI specific exceptions."""
    return JSONResponse(
        status_code=400,
        content={"error": str(exc), "type": exc.__class__.__name__}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc: Exception):
    """Handle general exceptions."""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "type": "InternalError"}
    )


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    try:
        # Check database connection
        # Check blockchain connections
        network_status = await blockchain_manager.get_all_network_status()
        
        healthy_networks = sum(1 for status in network_status.values() if status.get("connected", False))
        total_networks = len(network_status)
        
        return {
            "status": "healthy",
            "version": "0.1.0",
            "networks": {
                "total": total_networks,
                "healthy": healthy_networks,
                "details": network_status
            },
            "timestamp": asyncio.get_event_loop().time()
        }
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "error": str(e),
                "timestamp": asyncio.get_event_loop().time()
            }
        )


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "Nivora AI SDK API",
        "version": "0.1.0",
        "description": "Deploy, scale, and monetize AI agents across multiple blockchain networks",
        "docs": "/docs",
        "health": "/health",
        "websocket": "/ws",
        "links": {
            "website": "https://www.nivora-ai.com",
            "docs": "https://docs.app-nivoraai.com",
            "support": "support@nivora-ai.com",
            "telegram": "https://t.me/Nivora_AI",
            "twitter": "https://x.com/Nivora_AI",
            "github": "https://github.com/Nivora-AI"
        }
    }


# Include routers
app.include_router(
    agents.router,
    prefix="/api/v1/agents",
    tags=["agents"],
    dependencies=[Depends(verify_api_key)]
)

app.include_router(
    deployment.router,
    prefix="/api/v1/deployment",
    tags=["deployment"],
    dependencies=[Depends(verify_api_key)]
)

app.include_router(
    monitoring.router,
    prefix="/api/v1/monitoring",
    tags=["monitoring"],
    dependencies=[Depends(verify_api_key)]
)

app.include_router(
    monetization.router,
    prefix="/api/v1/monetization",
    tags=["monetization"],
    dependencies=[Depends(verify_api_key)]
)

# WebSocket endpoint
app.websocket("/ws")(websocket_endpoint)


if __name__ == "__main__":
    import uvicorn
    
    # Get configuration from environment
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    workers = int(os.getenv("WORKERS", "1"))
    
    logger.info(f"Starting Nivora AI API on {host}:{port}")
    
    if workers > 1:
        uvicorn.run(
            "nivora_ai.api.main:app",
            host=host,
            port=port,
            workers=workers,
            log_level="info"
        )
    else:
        uvicorn.run(
            app,
            host=host,
            port=port,
            log_level="info"
        )
