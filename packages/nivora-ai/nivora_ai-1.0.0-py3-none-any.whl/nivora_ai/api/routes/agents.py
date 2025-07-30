"""
Agent management API routes.
"""

from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.responses import JSONResponse

from ...core.agent import AIAgent, AgentConfig, AgentType, AgentStatus
from ...core.deployment import DeploymentConfig, ScalingStrategy
from ...database.schemas import AgentCreate, AgentUpdate, Agent as AgentSchema
from ...utils.logger import get_logger
from ...utils.exceptions import AgentError, DeploymentError

logger = get_logger(__name__)

router = APIRouter(prefix="/agents", tags=["agents"])


@router.post("/", response_model=AgentSchema)
async def create_agent(agent_data: AgentCreate):
    """Create a new AI agent."""
    try:
        # Create agent configuration
        agent_config = AgentConfig(
            name=agent_data.name,
            agent_type=agent_data.agent_type,
            description=agent_data.description,
            version=agent_data.version,
            networks=agent_data.networks,
            auto_scale=agent_data.auto_scale,
            max_instances=agent_data.max_instances,
            min_instances=agent_data.min_instances,
            monetization_enabled=agent_data.monetization_enabled,
            execution_parameters=agent_data.execution_parameters,
            environment_variables=agent_data.environment_variables,
            resource_limits=agent_data.resource_limits
        )
        
        # Create AI agent
        agent = AIAgent(agent_config)
        await agent.initialize()
        
        # Return agent information
        return AgentSchema(
            id=agent.agent_id,
            name=agent.config.name,
            agent_type=agent.config.agent_type,
            description=agent.config.description,
            version=agent.config.version,
            status=agent.status,
            networks=agent.config.networks,
            auto_scale=agent.config.auto_scale,
            max_instances=agent.config.max_instances,
            min_instances=agent.config.min_instances,
            monetization_enabled=agent.config.monetization_enabled,
            execution_parameters=agent.config.execution_parameters,
            environment_variables=agent.config.environment_variables,
            resource_limits=agent.config.resource_limits,
            metrics=agent.metrics,
            network_addresses=agent.network_addresses,
            deployment_id=None,
            created_at=agent.created_at,
            updated_at=agent.updated_at
        )
        
    except Exception as e:
        logger.error(f"Failed to create agent: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[AgentSchema])
async def list_agents(
    status: Optional[AgentStatus] = None,
    agent_type: Optional[AgentType] = None,
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0)
):
    """List all agents with optional filtering."""
    try:
        # This would typically query the database
        # For now, return empty list as placeholder
        agents = []
        
        return agents
        
    except Exception as e:
        logger.error(f"Failed to list agents: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve agents")


@router.get("/{agent_id}", response_model=AgentSchema)
async def get_agent(agent_id: str):
    """Get agent by ID."""
    try:
        # This would typically query the database
        # For now, return 404 as placeholder
        raise HTTPException(status_code=404, detail="Agent not found")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get agent {agent_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve agent")


@router.put("/{agent_id}", response_model=AgentSchema)
async def update_agent(agent_id: str, agent_update: AgentUpdate):
    """Update agent configuration."""
    try:
        # This would typically update the database
        # For now, return 404 as placeholder
        raise HTTPException(status_code=404, detail="Agent not found")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update agent {agent_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to update agent")


@router.delete("/{agent_id}")
async def delete_agent(agent_id: str):
    """Delete agent."""
    try:
        # This would typically delete from database and stop deployments
        # For now, return 404 as placeholder
        raise HTTPException(status_code=404, detail="Agent not found")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete agent {agent_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete agent")


@router.post("/{agent_id}/execute")
async def execute_agent_task(agent_id: str, task_data: Dict[str, Any]):
    """Execute a task with the agent."""
    try:
        # This would typically execute the task
        # For now, return success message as placeholder
        return {
            "message": "Task execution initiated",
            "agent_id": agent_id,
            "task_id": f"task_{agent_id}_{hash(str(task_data))}",
            "status": "pending"
        }
        
    except Exception as e:
        logger.error(f"Failed to execute task for agent {agent_id}: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{agent_id}/status")
async def get_agent_status(agent_id: str):
    """Get detailed agent status."""
    try:
        # This would typically get real status
        # For now, return sample status
        return {
            "agent_id": agent_id,
            "status": "active",
            "health": "healthy",
            "uptime": "2h 15m",
            "request_count": 127,
            "error_count": 2,
            "last_activity": "2024-01-15T10:30:00Z",
            "deployment_status": "deployed",
            "networks": ["ethereum", "polygon"],
            "performance_metrics": {
                "avg_response_time": 250,
                "success_rate": 98.4,
                "resource_usage": {
                    "cpu": 45.2,
                    "memory": 67.8
                }
            }
        }
        
    except Exception as e:
        logger.error(f"Failed to get status for agent {agent_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to get agent status")


@router.post("/{agent_id}/deploy")
async def deploy_agent(agent_id: str, deployment_config: Dict[str, Any]):
    """Deploy agent to specified networks."""
    try:
        # This would typically create deployment
        # For now, return success message
        return {
            "message": "Deployment initiated",
            "agent_id": agent_id,
            "deployment_id": f"deploy_{agent_id}_{hash(str(deployment_config))}",
            "target_networks": deployment_config.get("networks", []),
            "status": "deploying"
        }
        
    except Exception as e:
        logger.error(f"Failed to deploy agent {agent_id}: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{agent_id}/scale")
async def scale_agent(agent_id: str, scale_config: Dict[str, Any]):
    """Scale agent instances."""
    try:
        target_replicas = scale_config.get("replicas", 1)
        
        return {
            "message": "Scaling initiated",
            "agent_id": agent_id,
            "target_replicas": target_replicas,
            "status": "scaling"
        }
        
    except Exception as e:
        logger.error(f"Failed to scale agent {agent_id}: {e}")
        raise HTTPException(status_code=400, detail=str(e))