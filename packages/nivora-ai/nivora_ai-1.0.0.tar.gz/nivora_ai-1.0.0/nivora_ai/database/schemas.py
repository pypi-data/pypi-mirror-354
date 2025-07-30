"""
Pydantic schemas for database models.
"""

from datetime import datetime
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field, validator

from ..core.agent import AgentType, AgentStatus
from ..core.deployment import DeploymentStatus, ScalingStrategy
from ..core.monetization import PaymentModel, PaymentStatus, RevenueType


class AgentBase(BaseModel):
    """Base agent schema."""
    name: str = Field(..., min_length=3, max_length=100)
    agent_type: AgentType
    description: str = Field(..., min_length=10, max_length=1000)
    version: str = Field(default="1.0.0")
    networks: List[str] = Field(..., min_items=1)
    auto_scale: bool = Field(default=True)
    max_instances: int = Field(default=10, ge=1, le=100)
    min_instances: int = Field(default=1, ge=1)
    monetization_enabled: bool = Field(default=False)
    execution_parameters: Dict[str, Any] = Field(default_factory=dict)
    environment_variables: Dict[str, str] = Field(default_factory=dict)
    resource_limits: Dict[str, Any] = Field(default_factory=dict)


class AgentCreate(AgentBase):
    """Schema for creating an agent."""
    pass


class AgentUpdate(BaseModel):
    """Schema for updating an agent."""
    name: Optional[str] = Field(None, min_length=3, max_length=100)
    description: Optional[str] = Field(None, min_length=10, max_length=1000)
    version: Optional[str] = None
    auto_scale: Optional[bool] = None
    max_instances: Optional[int] = Field(None, ge=1, le=100)
    min_instances: Optional[int] = Field(None, ge=1)
    monetization_enabled: Optional[bool] = None
    execution_parameters: Optional[Dict[str, Any]] = None
    environment_variables: Optional[Dict[str, str]] = None
    resource_limits: Optional[Dict[str, Any]] = None


class Agent(AgentBase):
    """Agent schema with database fields."""
    id: str
    status: AgentStatus
    metrics: Dict[str, Any]
    network_addresses: Dict[str, str]
    deployment_id: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class DeploymentBase(BaseModel):
    """Base deployment schema."""
    agent_id: str = Field(..., min_length=1)
    target_networks: List[str] = Field(..., min_items=1)
    scaling_strategy: ScalingStrategy = Field(default=ScalingStrategy.REQUEST_BASED)
    auto_scaling_enabled: bool = Field(default=True)
    min_replicas: int = Field(default=1, ge=1, le=100)
    max_replicas: int = Field(default=10, ge=1, le=100)
    resource_requirements: Dict[str, Any] = Field(default_factory=dict)
    environment_variables: Dict[str, str] = Field(default_factory=dict)
    deployment_timeout: int = Field(default=300, ge=60, le=3600)
    health_check_enabled: bool = Field(default=True)
    monitoring_enabled: bool = Field(default=True)


class DeploymentCreate(DeploymentBase):
    """Schema for creating a deployment."""
    pass


class DeploymentUpdate(BaseModel):
    """Schema for updating a deployment."""
    scaling_strategy: Optional[ScalingStrategy] = None
    auto_scaling_enabled: Optional[bool] = None
    min_replicas: Optional[int] = Field(None, ge=1, le=100)
    max_replicas: Optional[int] = Field(None, ge=1, le=100)
    resource_requirements: Optional[Dict[str, Any]] = None
    environment_variables: Optional[Dict[str, str]] = None
    health_check_enabled: Optional[bool] = None
    monitoring_enabled: Optional[bool] = None


class Deployment(DeploymentBase):
    """Deployment schema with database fields."""
    id: str
    status: DeploymentStatus
    current_replicas: int
    healthy_replicas: int
    contract_addresses: Dict[str, str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class DeploymentInstanceBase(BaseModel):
    """Base deployment instance schema."""
    deployment_id: str = Field(..., min_length=1)
    network: str = Field(..., min_length=1)
    contract_address: Optional[str] = None
    status: str = Field(default="initializing")
    health_status: str = Field(default="unknown")
    error_message: Optional[str] = None
    metrics: Dict[str, Any] = Field(default_factory=dict)


class DeploymentInstance(DeploymentInstanceBase):
    """Deployment instance schema with database fields."""
    id: str
    last_health_check: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class PaymentConfigBase(BaseModel):
    """Base payment configuration schema."""
    agent_id: str = Field(..., min_length=1)
    payment_model: PaymentModel
    base_price: float = Field(..., gt=0)
    currency: str = Field(default="ETH", regex="^(ETH|MATIC|BNB|SOL|USDC|USDT)$")
    network: str = Field(..., min_length=1)
    token_address: Optional[str] = None
    revenue_share_percentage: Optional[float] = Field(None, ge=0, le=100)
    subscription_duration: Optional[int] = Field(None, ge=1)
    usage_limits: Dict[str, int] = Field(default_factory=dict)
    discount_tiers: List[Dict[str, Any]] = Field(default_factory=list)
    auto_renewal: bool = Field(default=False)


class PaymentConfigCreate(PaymentConfigBase):
    """Schema for creating a payment configuration."""
    
    @validator('revenue_share_percentage')
    def validate_revenue_share(cls, v, values):
        if values.get('payment_model') == PaymentModel.REVENUE_SHARE and v is None:
            raise ValueError('Revenue share percentage is required for revenue share model')
        return v
    
    @validator('subscription_duration')
    def validate_subscription_duration(cls, v, values):
        if values.get('payment_model') == PaymentModel.SUBSCRIPTION and v is None:
            raise ValueError('Subscription duration is required for subscription model')
        return v


class PaymentConfig(PaymentConfigBase):
    """Payment configuration schema with database fields."""
    id: str
    contract_address: Optional[str]
    enabled: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class PaymentRecordBase(BaseModel):
    """Base payment record schema."""
    payment_config_id: str = Field(..., min_length=1)
    agent_id: str = Field(..., min_length=1)
    user_address: str = Field(..., min_length=1)
    amount: float = Field(..., gt=0)
    currency: str = Field(..., min_length=1)
    network: str = Field(..., min_length=1)
    payment_model: PaymentModel
    status: PaymentStatus = Field(default=PaymentStatus.PENDING)
    transaction_hash: Optional[str] = None
    confirmation_blocks: int = Field(default=0)
    gas_used: Optional[int] = None
    gas_price: Optional[float] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class PaymentRecord(PaymentRecordBase):
    """Payment record schema with database fields."""
    id: str
    created_at: datetime
    confirmed_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class RevenueRecordBase(BaseModel):
    """Base revenue record schema."""
    agent_id: str = Field(..., min_length=1)
    revenue_type: RevenueType
    amount: float = Field(..., ge=0)
    currency: str = Field(..., min_length=1)
    network: str = Field(..., min_length=1)
    period_start: datetime
    period_end: datetime
    metadata: Dict[str, Any] = Field(default_factory=dict)


class RevenueRecord(RevenueRecordBase):
    """Revenue record schema with database fields."""
    id: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class CrossChainTransactionBase(BaseModel):
    """Base cross-chain transaction schema."""
    source_network: str = Field(..., min_length=1)
    destination_network: str = Field(..., min_length=1)
    bridge_type: str = Field(..., min_length=1)
    message_type: str = Field(..., min_length=1)
    status: str = Field(default="pending")
    source_tx_hash: Optional[str] = None
    destination_tx_hash: Optional[str] = None
    amount: Optional[float] = None
    token_address: Optional[str] = None
    sender_address: str = Field(..., min_length=1)
    recipient_address: str = Field(..., min_length=1)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    error_message: Optional[str] = None


class CrossChainTransaction(CrossChainTransactionBase):
    """Cross-chain transaction schema with database fields."""
    id: str
    created_at: datetime
    confirmed_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class NetworkStatusBase(BaseModel):
    """Base network status schema."""
    network_name: str = Field(..., min_length=1)
    network_type: str = Field(..., min_length=1)
    chain_id: Optional[int] = None
    block_height: int = Field(default=0)
    is_connected: bool = Field(default=False)
    gas_price: Optional[float] = None
    response_time: Optional[float] = None
    last_block_time: Optional[datetime] = None
    error_message: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class NetworkStatus(NetworkStatusBase):
    """Network status schema with database fields."""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class AlertRuleBase(BaseModel):
    """Base alert rule schema."""
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    metric: str = Field(..., min_length=1)
    operator: str = Field(..., regex="^(gt|lt|gte|lte|eq|ne)$")
    threshold: float
    duration: int = Field(default=300, ge=60)
    severity: str = Field(default="warning", regex="^(info|warning|error|critical)$")
    enabled: bool = Field(default=True)
    notification_channels: List[str] = Field(default_factory=list)
    agent_id: Optional[str] = None
    deployment_id: Optional[str] = None
    created_by: Optional[str] = None


class AlertRuleCreate(AlertRuleBase):
    """Schema for creating an alert rule."""
    pass


class AlertRule(AlertRuleBase):
    """Alert rule schema with database fields."""
    id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class AlertBase(BaseModel):
    """Base alert schema."""
    rule_id: str = Field(..., min_length=1)
    agent_id: Optional[str] = None
    deployment_id: Optional[str] = None
    metric: str = Field(..., min_length=1)
    current_value: float
    threshold: float
    severity: str = Field(..., regex="^(info|warning|error|critical)$")
    status: str = Field(default="active", regex="^(active|resolved|suppressed)$")
    message: str = Field(..., min_length=1)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    resolved_at: Optional[datetime] = None
    acknowledged_at: Optional[datetime] = None
    acknowledged_by: Optional[str] = None


class Alert(AlertBase):
    """Alert schema with database fields."""
    id: str
    fired_at: datetime
    
    class Config:
        from_attributes = True


# Query and response schemas
class AgentQuery(BaseModel):
    """Query parameters for agents."""
    status: Optional[AgentStatus] = None
    agent_type: Optional[AgentType] = None
    network: Optional[str] = None
    limit: int = Field(default=100, ge=1, le=1000)
    offset: int = Field(default=0, ge=0)


class DeploymentQuery(BaseModel):
    """Query parameters for deployments."""
    status: Optional[DeploymentStatus] = None
    agent_id: Optional[str] = None
    network: Optional[str] = None
    limit: int = Field(default=100, ge=1, le=1000)
    offset: int = Field(default=0, ge=0)


class PaymentQuery(BaseModel):
    """Query parameters for payments."""
    agent_id: Optional[str] = None
    user_address: Optional[str] = None
    status: Optional[PaymentStatus] = None
    payment_model: Optional[PaymentModel] = None
    network: Optional[str] = None
    limit: int = Field(default=100, ge=1, le=1000)
    offset: int = Field(default=0, ge=0)


class RevenueQuery(BaseModel):
    """Query parameters for revenue."""
    agent_id: Optional[str] = None
    revenue_type: Optional[RevenueType] = None
    currency: Optional[str] = None
    network: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    limit: int = Field(default=100, ge=1, le=1000)
    offset: int = Field(default=0, ge=0)


class PaginatedResponse(BaseModel):
    """Generic paginated response."""
    items: List[Any]
    total: int
    limit: int
    offset: int
    has_next: bool
    has_prev: bool


class HealthCheck(BaseModel):
    """Health check response schema."""
    status: str
    version: str
    timestamp: datetime
    database: bool
    networks: Dict[str, bool]
    services: Dict[str, bool]
