"""
Deployment management for Nivora AI SDK.
"""

import asyncio
import uuid
from datetime import datetime
from enum import Enum
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field

from ..utils.logger import get_logger
from ..utils.exceptions import DeploymentError, NetworkError
from .agent import AIAgent, AgentStatus

logger = get_logger(__name__)


class DeploymentStatus(Enum):
    """Deployment status enumeration."""
    PENDING = "pending"
    DEPLOYING = "deploying"
    DEPLOYED = "deployed"
    SCALING = "scaling"
    UPDATING = "updating"
    FAILED = "failed"
    TERMINATED = "terminated"


class ScalingStrategy(Enum):
    """Scaling strategy enumeration."""
    MANUAL = "manual"
    REQUEST_BASED = "request_based"
    RESOURCE_BASED = "resource_based"
    PREDICTIVE = "predictive"
    HYBRID = "hybrid"


@dataclass
class DeploymentConfig:
    """Configuration for deployment."""
    agent_id: str
    target_networks: List[str]
    scaling_strategy: ScalingStrategy = ScalingStrategy.REQUEST_BASED
    auto_scaling_enabled: bool = True
    min_replicas: int = 1
    max_replicas: int = 10
    resource_requirements: Dict[str, Any] = field(default_factory=dict)
    environment_variables: Dict[str, str] = field(default_factory=dict)
    deployment_timeout: int = 300
    health_check_enabled: bool = True
    monitoring_enabled: bool = True


@dataclass
class DeploymentInstance:
    """Represents a deployment instance."""
    id: str
    deployment_id: str
    network: str
    contract_address: Optional[str] = None
    status: str = "initializing"
    health_status: str = "unknown"
    error_message: Optional[str] = None
    metrics: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)


class DeploymentManager:
    """
    Manages AI agent deployments across multiple blockchain networks.
    """
    
    def __init__(self):
        """Initialize deployment manager."""
        self.deployments: Dict[str, Dict[str, Any]] = {}
        self.instances: Dict[str, DeploymentInstance] = {}
        self.scaling_metrics: Dict[str, Dict[str, Any]] = {}
        self.event_handlers: Dict[str, List[Callable]] = {}
        
    def add_event_handler(self, event: str, handler: Callable) -> None:
        """Add event handler for deployment lifecycle events."""
        if event not in self.event_handlers:
            self.event_handlers[event] = []
        self.event_handlers[event].append(handler)
    
    def emit_event(self, event: str, data: Dict[str, Any] = None) -> None:
        """Emit event to registered handlers."""
        if event in self.event_handlers:
            for handler in self.event_handlers[event]:
                try:
                    event_data = data if data is not None else {}
                    if asyncio.iscoroutinefunction(handler):
                        asyncio.create_task(handler(event_data))
                    else:
                        handler(event_data)
                except Exception as e:
                    logger.error(f"Error in event handler for {event}: {e}")
    
    async def create_deployment(self, config: DeploymentConfig) -> str:
        """Create a new deployment."""
        try:
            deployment_id = str(uuid.uuid4())
            
            deployment = {
                "id": deployment_id,
                "agent_id": config.agent_id,
                "status": DeploymentStatus.PENDING,
                "config": config,
                "target_networks": config.target_networks,
                "scaling_strategy": config.scaling_strategy,
                "auto_scaling_enabled": config.auto_scaling_enabled,
                "min_replicas": config.min_replicas,
                "max_replicas": config.max_replicas,
                "current_replicas": 0,
                "healthy_replicas": 0,
                "resource_requirements": config.resource_requirements,
                "environment_variables": config.environment_variables,
                "deployment_timeout": config.deployment_timeout,
                "health_check_enabled": config.health_check_enabled,
                "monitoring_enabled": config.monitoring_enabled,
                "contract_addresses": {},
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
            
            self.deployments[deployment_id] = deployment
            
            # Initialize scaling metrics
            self.scaling_metrics[deployment_id] = {
                "request_count": 0,
                "response_time": 0,
                "cpu_usage": 0,
                "memory_usage": 0,
                "error_rate": 0,
                "last_updated": datetime.utcnow()
            }
            
            logger.info(f"Deployment created: {deployment_id}")
            
            self.emit_event("deployment_created", {
                "deployment_id": deployment_id,
                "agent_id": config.agent_id,
                "networks": config.target_networks
            })
            
            return deployment_id
            
        except Exception as e:
            logger.error(f"Failed to create deployment: {e}")
            raise DeploymentError(f"Deployment creation failed: {e}")
    
    async def deploy_agent(self, deployment_id: str, agent: AIAgent, blockchain_manager) -> bool:
        """Deploy agent to specified networks."""
        try:
            if deployment_id not in self.deployments:
                raise DeploymentError(f"Deployment not found: {deployment_id}")
            
            deployment = self.deployments[deployment_id]
            deployment["status"] = DeploymentStatus.DEPLOYING
            deployment["updated_at"] = datetime.utcnow()
            
            # Deploy to each target network
            successful_deployments = []
            failed_deployments = []
            
            for network in deployment["target_networks"]:
                try:
                    logger.info(f"Deploying to network: {network}")
                    
                    # Create deployment instance
                    instance_id = str(uuid.uuid4())
                    instance = DeploymentInstance(
                        id=instance_id,
                        deployment_id=deployment_id,
                        network=network,
                        status="deploying"
                    )
                    
                    self.instances[instance_id] = instance
                    
                    # Deploy to blockchain network
                    contract_address = await self._deploy_to_network(
                        network, agent, blockchain_manager
                    )
                    
                    if contract_address:
                        instance.contract_address = contract_address
                        instance.status = "deployed"
                        instance.health_status = "healthy"
                        instance.updated_at = datetime.utcnow()
                        
                        deployment["contract_addresses"][network] = contract_address
                        successful_deployments.append(network)
                        
                        logger.info(f"Successfully deployed to {network}: {contract_address}")
                    else:
                        instance.status = "failed"
                        instance.error_message = "Contract deployment failed"
                        failed_deployments.append(network)
                        
                except Exception as e:
                    logger.error(f"Failed to deploy to {network}: {e}")
                    instance.status = "failed"
                    instance.error_message = str(e)
                    failed_deployments.append(network)
            
            # Update deployment status
            if successful_deployments:
                if failed_deployments:
                    deployment["status"] = DeploymentStatus.DEPLOYED  # Partial success
                else:
                    deployment["status"] = DeploymentStatus.DEPLOYED
                    
                deployment["current_replicas"] = len(successful_deployments)
                deployment["healthy_replicas"] = len(successful_deployments)
                
                # Update agent status
                agent.update_status(AgentStatus.ACTIVE)
                agent.network_addresses = deployment["contract_addresses"]
                
                self.emit_event("deployment_success", {
                    "deployment_id": deployment_id,
                    "agent_id": deployment["agent_id"],
                    "successful_networks": successful_deployments,
                    "failed_networks": failed_deployments
                })
                
                # Start monitoring if enabled
                if deployment["monitoring_enabled"]:
                    asyncio.create_task(self._start_monitoring(deployment_id))
                
                return True
            else:
                deployment["status"] = DeploymentStatus.FAILED
                agent.update_status(AgentStatus.ERROR)
                
                self.emit_event("deployment_failed", {
                    "deployment_id": deployment_id,
                    "agent_id": deployment["agent_id"],
                    "error": "All network deployments failed"
                })
                
                return False
                
        except Exception as e:
            logger.error(f"Deployment failed: {e}")
            if deployment_id in self.deployments:
                self.deployments[deployment_id]["status"] = DeploymentStatus.FAILED
            raise DeploymentError(f"Agent deployment failed: {e}")
    
    async def _deploy_to_network(self, network: str, agent: AIAgent, blockchain_manager) -> Optional[str]:
        """Deploy agent to a specific network."""
        try:
            # Get network instance
            network_instance = blockchain_manager.get_network(network)
            if not network_instance:
                raise NetworkError(f"Network not configured: {network}")
            
            # Generate smart contract code based on agent type
            contract_code = self._generate_contract_code(agent)
            
            # Deploy contract
            contract_address = await network_instance.deploy_contract(
                contract_code,
                constructor_args=[agent.config.name, agent.config.version]
            )
            
            return contract_address
            
        except Exception as e:
            logger.error(f"Failed to deploy to {network}: {e}")
            return None
    
    def _generate_contract_code(self, agent: AIAgent) -> str:
        """Generate smart contract code for the agent."""
        # This is a simplified contract template
        # In a real implementation, this would be more sophisticated
        contract_template = f"""
        pragma solidity ^0.8.0;
        
        contract NivoraAgent {{
            string public name;
            string public version;
            string public agentType;
            address public owner;
            
            constructor(string memory _name, string memory _version) {{
                name = _name;
                version = _version;
                agentType = "{agent.config.agent_type.value}";
                owner = msg.sender;
            }}
            
            function execute(bytes calldata data) external returns (bytes memory) {{
                // Agent execution logic would go here
                return data;
            }}
        }}
        """
        return contract_template
    
    async def scale_deployment(self, deployment_id: str, target_replicas: int) -> bool:
        """Scale deployment to target number of replicas."""
        try:
            if deployment_id not in self.deployments:
                raise DeploymentError(f"Deployment not found: {deployment_id}")
            
            deployment = self.deployments[deployment_id]
            current_replicas = deployment["current_replicas"]
            
            if target_replicas == current_replicas:
                return True
            
            deployment["status"] = DeploymentStatus.SCALING
            
            if target_replicas > current_replicas:
                # Scale up
                await self._scale_up(deployment_id, target_replicas - current_replicas)
            else:
                # Scale down
                await self._scale_down(deployment_id, current_replicas - target_replicas)
            
            deployment["current_replicas"] = target_replicas
            deployment["status"] = DeploymentStatus.DEPLOYED
            deployment["updated_at"] = datetime.utcnow()
            
            self.emit_event("deployment_scaled", {
                "deployment_id": deployment_id,
                "previous_replicas": current_replicas,
                "new_replicas": target_replicas
            })
            
            return True
            
        except Exception as e:
            logger.error(f"Scaling failed for {deployment_id}: {e}")
            raise DeploymentError(f"Scaling failed: {e}")
    
    async def _scale_up(self, deployment_id: str, additional_replicas: int) -> None:
        """Scale up deployment by adding replicas."""
        # Implementation would create additional instances
        logger.info(f"Scaling up deployment {deployment_id} by {additional_replicas} replicas")
    
    async def _scale_down(self, deployment_id: str, remove_replicas: int) -> None:
        """Scale down deployment by removing replicas."""
        # Implementation would remove instances
        logger.info(f"Scaling down deployment {deployment_id} by {remove_replicas} replicas")
    
    async def terminate_deployment(self, deployment_id: str) -> bool:
        """Terminate a deployment."""
        try:
            if deployment_id not in self.deployments:
                raise DeploymentError(f"Deployment not found: {deployment_id}")
            
            deployment = self.deployments[deployment_id]
            deployment["status"] = DeploymentStatus.TERMINATED
            deployment["current_replicas"] = 0
            deployment["healthy_replicas"] = 0
            deployment["updated_at"] = datetime.utcnow()
            
            # Terminate all instances
            instances_to_remove = []
            for instance_id, instance in self.instances.items():
                if instance.deployment_id == deployment_id:
                    instance.status = "terminated"
                    instances_to_remove.append(instance_id)
            
            for instance_id in instances_to_remove:
                del self.instances[instance_id]
            
            self.emit_event("deployment_terminated", {
                "deployment_id": deployment_id,
                "agent_id": deployment["agent_id"]
            })
            
            logger.info(f"Deployment terminated: {deployment_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to terminate deployment {deployment_id}: {e}")
            raise DeploymentError(f"Termination failed: {e}")
    
    async def _start_monitoring(self, deployment_id: str) -> None:
        """Start monitoring for a deployment."""
        logger.info(f"Starting monitoring for deployment: {deployment_id}")
        
        while deployment_id in self.deployments:
            try:
                deployment = self.deployments[deployment_id]
                if deployment["status"] == DeploymentStatus.TERMINATED:
                    break
                
                # Check health of instances
                await self._health_check(deployment_id)
                
                # Auto-scaling logic
                if deployment["auto_scaling_enabled"]:
                    await self._auto_scale_check(deployment_id)
                
                # Wait before next check
                await asyncio.sleep(30)
                
            except Exception as e:
                logger.error(f"Monitoring error for {deployment_id}: {e}")
                await asyncio.sleep(60)  # Wait longer on error
    
    async def _health_check(self, deployment_id: str) -> None:
        """Perform health check on deployment instances."""
        deployment = self.deployments[deployment_id]
        healthy_count = 0
        
        for instance_id, instance in self.instances.items():
            if instance.deployment_id == deployment_id:
                # Simulate health check
                instance.health_status = "healthy"  # In real implementation, this would be actual checks
                instance.last_health_check = datetime.utcnow()
                if instance.health_status == "healthy":
                    healthy_count += 1
        
        deployment["healthy_replicas"] = healthy_count
    
    async def _auto_scale_check(self, deployment_id: str) -> None:
        """Check if auto-scaling is needed."""
        deployment = self.deployments[deployment_id]
        metrics = self.scaling_metrics.get(deployment_id, {})
        
        current_replicas = deployment["current_replicas"]
        min_replicas = deployment["min_replicas"]
        max_replicas = deployment["max_replicas"]
        
        # Simple scaling logic based on request count
        request_count = metrics.get("request_count", 0)
        
        if request_count > current_replicas * 100 and current_replicas < max_replicas:
            # Scale up
            await self.scale_deployment(deployment_id, min(current_replicas + 1, max_replicas))
        elif request_count < current_replicas * 50 and current_replicas > min_replicas:
            # Scale down
            await self.scale_deployment(deployment_id, max(current_replicas - 1, min_replicas))
    
    def get_deployment_status(self, deployment_id: str) -> Optional[Dict[str, Any]]:
        """Get deployment status information."""
        if deployment_id not in self.deployments:
            return None
        
        deployment = self.deployments[deployment_id]
        instances = [
            instance for instance in self.instances.values()
            if instance.deployment_id == deployment_id
        ]
        
        return {
            "deployment_id": deployment_id,
            "status": deployment["status"],
            "agent_id": deployment["agent_id"],
            "target_networks": deployment["target_networks"],
            "current_replicas": deployment["current_replicas"],
            "healthy_replicas": deployment["healthy_replicas"],
            "contract_addresses": deployment["contract_addresses"],
            "instances": [
                {
                    "id": instance.id,
                    "network": instance.network,
                    "status": instance.status,
                    "health_status": instance.health_status,
                    "contract_address": instance.contract_address
                } for instance in instances
            ],
            "metrics": self.scaling_metrics.get(deployment_id, {}),
            "created_at": deployment["created_at"],
            "updated_at": deployment["updated_at"]
        }
    
    def get_all_deployments(self) -> Dict[str, Dict[str, Any]]:
        """Get status of all deployments."""
        return {
            deployment_id: self.get_deployment_status(deployment_id)
            for deployment_id in self.deployments.keys()
        }