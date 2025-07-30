"""
Core AI Agent implementation for Nivora AI SDK.
"""

import uuid
import asyncio
from typing import Dict, Any, Optional, List, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

from ..utils.logger import get_logger
from ..utils.exceptions import AgentException, ValidationException

logger = get_logger(__name__)


class AgentStatus(Enum):
    """Agent status enumeration."""
    INACTIVE = "inactive"
    DEPLOYING = "deploying"
    ACTIVE = "active"
    SCALING = "scaling"
    ERROR = "error"
    TERMINATED = "terminated"


class AgentType(Enum):
    """Agent type enumeration."""
    TRADING = "trading"
    DEFI = "defi"
    NFT = "nft"
    ANALYTICS = "analytics"
    GOVERNANCE = "governance"
    CUSTOM = "custom"


@dataclass
class AgentConfig:
    """Configuration for AI Agent deployment."""
    name: str
    agent_type: AgentType
    description: str
    version: str = "1.0.0"
    networks: List[str] = field(default_factory=list)
    auto_scale: bool = True
    max_instances: int = 10
    min_instances: int = 1
    monetization_enabled: bool = False
    execution_parameters: Dict[str, Any] = field(default_factory=dict)
    environment_variables: Dict[str, str] = field(default_factory=dict)
    resource_limits: Dict[str, Any] = field(default_factory=dict)
    
    def validate(self) -> bool:
        """Validate agent configuration."""
        if not self.name or len(self.name) < 3:
            raise ValidationException("Agent name must be at least 3 characters long")
        
        if not self.networks:
            raise ValidationException("At least one network must be specified")
        
        if self.max_instances < self.min_instances:
            raise ValidationException("max_instances must be greater than or equal to min_instances")
        
        return True


class AIAgent:
    """
    Core AI Agent class for blockchain deployment and management.
    """
    
    def __init__(self, config: AgentConfig):
        """Initialize AI Agent with configuration."""
        config.validate()
        
        self.id = str(uuid.uuid4())
        self.config = config
        self.status = AgentStatus.INACTIVE
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        self.deployment_id: Optional[str] = None
        self.network_addresses: Dict[str, str] = {}
        self.metrics: Dict[str, Any] = {}
        self.event_handlers: Dict[str, List[Callable]] = {}
        
        logger.info(f"Created AI Agent {self.id} with name '{config.name}'")
    
    def add_event_handler(self, event: str, handler: Callable) -> None:
        """Add event handler for agent lifecycle events."""
        if event not in self.event_handlers:
            self.event_handlers[event] = []
        self.event_handlers[event].append(handler)
    
    def emit_event(self, event: str, data: Dict[str, Any] = None) -> None:
        """Emit event to registered handlers."""
        if event in self.event_handlers:
            for handler in self.event_handlers[event]:
                try:
                    handler(self, event, data or {})
                except Exception as e:
                    logger.error(f"Error in event handler for {event}: {e}")
    
    async def initialize(self) -> None:
        """Initialize agent for deployment."""
        try:
            self.status = AgentStatus.DEPLOYING
            self.updated_at = datetime.utcnow()
            
            # Initialize agent-specific logic here
            await self._setup_agent_logic()
            
            self.emit_event("agent_initialized", {"agent_id": self.id})
            logger.info(f"Agent {self.id} initialized successfully")
            
        except Exception as e:
            self.status = AgentStatus.ERROR
            self.emit_event("agent_error", {"error": str(e)})
            raise AgentException(f"Failed to initialize agent: {e}")
    
    async def _setup_agent_logic(self) -> None:
        """Setup agent-specific logic based on agent type."""
        setup_methods = {
            AgentType.TRADING: self._setup_trading_agent,
            AgentType.DEFI: self._setup_defi_agent,
            AgentType.NFT: self._setup_nft_agent,
            AgentType.ANALYTICS: self._setup_analytics_agent,
            AgentType.GOVERNANCE: self._setup_governance_agent,
            AgentType.CUSTOM: self._setup_custom_agent,
        }
        
        setup_method = setup_methods.get(self.config.agent_type)
        if setup_method:
            await setup_method()
    
    async def _setup_trading_agent(self) -> None:
        """Setup trading agent logic."""
        # Initialize trading-specific components
        self.metrics["trading_pairs"] = []
        self.metrics["total_trades"] = 0
        self.metrics["profit_loss"] = 0.0
    
    async def _setup_defi_agent(self) -> None:
        """Setup DeFi agent logic."""
        # Initialize DeFi-specific components
        self.metrics["protocols"] = []
        self.metrics["total_value_locked"] = 0.0
        self.metrics["yield_earned"] = 0.0
    
    async def _setup_nft_agent(self) -> None:
        """Setup NFT agent logic."""
        # Initialize NFT-specific components
        self.metrics["collections"] = []
        self.metrics["nfts_minted"] = 0
        self.metrics["royalties_earned"] = 0.0
    
    async def _setup_analytics_agent(self) -> None:
        """Setup analytics agent logic."""
        # Initialize analytics-specific components
        self.metrics["data_sources"] = []
        self.metrics["reports_generated"] = 0
        self.metrics["insights_provided"] = 0
    
    async def _setup_governance_agent(self) -> None:
        """Setup governance agent logic."""
        # Initialize governance-specific components
        self.metrics["proposals_created"] = 0
        self.metrics["votes_cast"] = 0
        self.metrics["dao_participations"] = []
    
    async def _setup_custom_agent(self) -> None:
        """Setup custom agent logic."""
        # Initialize custom agent based on execution parameters
        for key, value in self.config.execution_parameters.items():
            self.metrics[key] = value
    
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute agent task."""
        if self.status != AgentStatus.ACTIVE:
            raise AgentException(f"Agent {self.id} is not active. Current status: {self.status}")
        
        try:
            self.emit_event("task_started", {"task": task})
            
            # Execute task based on agent type
            result = await self._execute_task(task)
            
            self.emit_event("task_completed", {"task": task, "result": result})
            return result
            
        except Exception as e:
            self.emit_event("task_failed", {"task": task, "error": str(e)})
            raise AgentException(f"Task execution failed: {e}")
    
    async def _execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute task based on agent type."""
        execution_methods = {
            AgentType.TRADING: self._execute_trading_task,
            AgentType.DEFI: self._execute_defi_task,
            AgentType.NFT: self._execute_nft_task,
            AgentType.ANALYTICS: self._execute_analytics_task,
            AgentType.GOVERNANCE: self._execute_governance_task,
            AgentType.CUSTOM: self._execute_custom_task,
        }
        
        execution_method = execution_methods.get(self.config.agent_type)
        if execution_method:
            return await execution_method(task)
        
        return {"status": "completed", "message": "Task executed successfully"}
    
    async def _execute_trading_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute trading-specific task."""
        # Implement trading logic
        action = task.get("action", "analyze")
        
        if action == "trade":
            # Execute trade
            self.metrics["total_trades"] += 1
            return {"status": "trade_executed", "trade_id": str(uuid.uuid4())}
        elif action == "analyze":
            # Analyze market
            return {"status": "analysis_complete", "signals": []}
        
        return {"status": "completed"}
    
    async def _execute_defi_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute DeFi-specific task."""
        # Implement DeFi logic
        action = task.get("action", "monitor")
        
        if action == "yield_farm":
            # Execute yield farming
            return {"status": "yield_farming_started", "pool_id": task.get("pool_id")}
        elif action == "liquidity_provide":
            # Provide liquidity
            return {"status": "liquidity_provided", "amount": task.get("amount")}
        
        return {"status": "completed"}
    
    async def _execute_nft_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute NFT-specific task."""
        # Implement NFT logic
        action = task.get("action", "monitor")
        
        if action == "mint":
            # Mint NFT
            self.metrics["nfts_minted"] += 1
            return {"status": "nft_minted", "token_id": str(uuid.uuid4())}
        elif action == "trade":
            # Trade NFT
            return {"status": "nft_traded", "transaction_id": str(uuid.uuid4())}
        
        return {"status": "completed"}
    
    async def _execute_analytics_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute analytics-specific task."""
        # Implement analytics logic
        action = task.get("action", "analyze")
        
        if action == "generate_report":
            # Generate analytics report
            self.metrics["reports_generated"] += 1
            return {"status": "report_generated", "report_id": str(uuid.uuid4())}
        elif action == "monitor":
            # Monitor blockchain data
            return {"status": "monitoring_active", "data_points": []}
        
        return {"status": "completed"}
    
    async def _execute_governance_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute governance-specific task."""
        # Implement governance logic
        action = task.get("action", "monitor")
        
        if action == "vote":
            # Cast vote
            self.metrics["votes_cast"] += 1
            return {"status": "vote_cast", "proposal_id": task.get("proposal_id")}
        elif action == "propose":
            # Create proposal
            self.metrics["proposals_created"] += 1
            return {"status": "proposal_created", "proposal_id": str(uuid.uuid4())}
        
        return {"status": "completed"}
    
    async def _execute_custom_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute custom task based on configuration."""
        # Implement custom logic based on execution parameters
        custom_handler = self.config.execution_parameters.get("task_handler")
        if custom_handler:
            # Execute custom handler if provided
            pass
        
        return {"status": "completed", "custom_result": task}
    
    def update_status(self, status: AgentStatus) -> None:
        """Update agent status."""
        old_status = self.status
        self.status = status
        self.updated_at = datetime.utcnow()
        
        self.emit_event("status_changed", {
            "old_status": old_status.value,
            "new_status": status.value
        })
        
        logger.info(f"Agent {self.id} status changed from {old_status.value} to {status.value}")
    
    def update_metrics(self, metrics: Dict[str, Any]) -> None:
        """Update agent metrics."""
        self.metrics.update(metrics)
        self.updated_at = datetime.utcnow()
        
        self.emit_event("metrics_updated", {"metrics": metrics})
    
    def get_status_info(self) -> Dict[str, Any]:
        """Get comprehensive agent status information."""
        return {
            "id": self.id,
            "name": self.config.name,
            "type": self.config.agent_type.value,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "deployment_id": self.deployment_id,
            "networks": self.config.networks,
            "network_addresses": self.network_addresses,
            "metrics": self.metrics,
            "config": {
                "version": self.config.version,
                "auto_scale": self.config.auto_scale,
                "max_instances": self.config.max_instances,
                "min_instances": self.config.min_instances,
                "monetization_enabled": self.config.monetization_enabled,
            }
        }
