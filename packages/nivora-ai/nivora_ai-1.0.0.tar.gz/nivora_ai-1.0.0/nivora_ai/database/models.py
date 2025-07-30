"""
Database models for Nivora AI SDK.
"""

import os
from datetime import datetime
from typing import Optional, AsyncGenerator
from sqlalchemy import (
    Column, String, Integer, Float, DateTime, Boolean, Text, JSON,
    ForeignKey, Index, create_engine, MetaData
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import relationship, Session, sessionmaker

from ..utils.logger import get_logger

logger = get_logger(__name__)

# Database URL from environment variables
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://nivora:nivora@localhost:5432/nivora_ai"
)

# Convert to async URL if needed
if DATABASE_URL.startswith("postgresql://"):
    ASYNC_DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")
else:
    ASYNC_DATABASE_URL = DATABASE_URL

# Create async engine
engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# Create sync engine for migration purposes
sync_engine = create_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True
)

SyncSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)

# Base class for all models
Base = declarative_base()
metadata = MetaData()


class Agent(Base):
    """Agent model."""
    __tablename__ = "agents"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    agent_type = Column(String(50), nullable=False, index=True)
    description = Column(Text, nullable=False)
    version = Column(String(20), nullable=False, default="1.0.0")
    status = Column(String(20), nullable=False, default="inactive", index=True)
    networks = Column(JSON, nullable=False, default=list)
    auto_scale = Column(Boolean, nullable=False, default=True)
    max_instances = Column(Integer, nullable=False, default=10)
    min_instances = Column(Integer, nullable=False, default=1)
    monetization_enabled = Column(Boolean, nullable=False, default=False)
    execution_parameters = Column(JSON, nullable=False, default=dict)
    environment_variables = Column(JSON, nullable=False, default=dict)
    resource_limits = Column(JSON, nullable=False, default=dict)
    metrics = Column(JSON, nullable=False, default=dict)
    network_addresses = Column(JSON, nullable=False, default=dict)
    deployment_id = Column(String, ForeignKey("deployments.id"), nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    deployment = relationship("Deployment", back_populates="agent")
    payment_configs = relationship("PaymentConfig", back_populates="agent")
    revenue_records = relationship("RevenueRecord", back_populates="agent")
    
    # Indexes
    __table_args__ = (
        Index("idx_agent_type_status", "agent_type", "status"),
        Index("idx_agent_created_at", "created_at"),
    )


class Deployment(Base):
    """Deployment model."""
    __tablename__ = "deployments"
    
    id = Column(String, primary_key=True, index=True)
    agent_id = Column(String, ForeignKey("agents.id"), nullable=False)
    status = Column(String(20), nullable=False, default="pending", index=True)
    target_networks = Column(JSON, nullable=False, default=list)
    scaling_strategy = Column(String(50), nullable=False, default="request_based")
    auto_scaling_enabled = Column(Boolean, nullable=False, default=True)
    min_replicas = Column(Integer, nullable=False, default=1)
    max_replicas = Column(Integer, nullable=False, default=10)
    current_replicas = Column(Integer, nullable=False, default=0)
    healthy_replicas = Column(Integer, nullable=False, default=0)
    resource_requirements = Column(JSON, nullable=False, default=dict)
    environment_variables = Column(JSON, nullable=False, default=dict)
    contract_addresses = Column(JSON, nullable=False, default=dict)
    deployment_timeout = Column(Integer, nullable=False, default=300)
    health_check_enabled = Column(Boolean, nullable=False, default=True)
    monitoring_enabled = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    agent = relationship("Agent", back_populates="deployment")
    instances = relationship("DeploymentInstance", back_populates="deployment")
    
    # Indexes
    __table_args__ = (
        Index("idx_deployment_status_created", "status", "created_at"),
        Index("idx_deployment_agent_id", "agent_id"),
    )


class DeploymentInstance(Base):
    """Deployment instance model."""
    __tablename__ = "deployment_instances"
    
    id = Column(String, primary_key=True, index=True)
    deployment_id = Column(String, ForeignKey("deployments.id"), nullable=False)
    network = Column(String(50), nullable=False, index=True)
    contract_address = Column(String, nullable=True)
    status = Column(String(20), nullable=False, default="initializing", index=True)
    health_status = Column(String(20), nullable=False, default="unknown")
    last_health_check = Column(DateTime, nullable=True)
    error_message = Column(Text, nullable=True)
    metrics = Column(JSON, nullable=False, default=dict)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    deployment = relationship("Deployment", back_populates="instances")
    
    # Indexes
    __table_args__ = (
        Index("idx_instance_deployment_network", "deployment_id", "network"),
        Index("idx_instance_status_health", "status", "health_status"),
    )


class PaymentConfig(Base):
    """Payment configuration model."""
    __tablename__ = "payment_configs"
    
    id = Column(String, primary_key=True, index=True)
    agent_id = Column(String, ForeignKey("agents.id"), nullable=False)
    payment_model = Column(String(50), nullable=False, index=True)
    base_price = Column(Float, nullable=False)
    currency = Column(String(10), nullable=False, default="ETH")
    network = Column(String(50), nullable=False)
    token_address = Column(String, nullable=True)
    revenue_share_percentage = Column(Float, nullable=True)
    subscription_duration = Column(Integer, nullable=True)  # days
    usage_limits = Column(JSON, nullable=False, default=dict)
    discount_tiers = Column(JSON, nullable=False, default=list)
    auto_renewal = Column(Boolean, nullable=False, default=False)
    contract_address = Column(String, nullable=True)
    enabled = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    agent = relationship("Agent", back_populates="payment_configs")
    payment_records = relationship("PaymentRecord", back_populates="payment_config")
    
    # Indexes
    __table_args__ = (
        Index("idx_payment_config_agent_model", "agent_id", "payment_model"),
        Index("idx_payment_config_network", "network"),
    )


class PaymentRecord(Base):
    """Payment record model."""
    __tablename__ = "payment_records"
    
    id = Column(String, primary_key=True, index=True)
    payment_config_id = Column(String, ForeignKey("payment_configs.id"), nullable=False)
    agent_id = Column(String, ForeignKey("agents.id"), nullable=False)
    user_address = Column(String, nullable=False, index=True)
    amount = Column(Float, nullable=False)
    currency = Column(String(10), nullable=False)
    network = Column(String(50), nullable=False)
    payment_model = Column(String(50), nullable=False)
    status = Column(String(20), nullable=False, default="pending", index=True)
    transaction_hash = Column(String, nullable=True, index=True)
    confirmation_blocks = Column(Integer, nullable=False, default=0)
    gas_used = Column(Integer, nullable=True)
    gas_price = Column(Float, nullable=True)
    metadata = Column(JSON, nullable=False, default=dict)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    confirmed_at = Column(DateTime, nullable=True)
    
    # Relationships
    payment_config = relationship("PaymentConfig", back_populates="payment_records")
    
    # Indexes
    __table_args__ = (
        Index("idx_payment_record_agent_user", "agent_id", "user_address"),
        Index("idx_payment_record_status_created", "status", "created_at"),
        Index("idx_payment_record_tx_hash", "transaction_hash"),
    )


class RevenueRecord(Base):
    """Revenue record model."""
    __tablename__ = "revenue_records"
    
    id = Column(String, primary_key=True, index=True)
    agent_id = Column(String, ForeignKey("agents.id"), nullable=False)
    revenue_type = Column(String(50), nullable=False, index=True)
    amount = Column(Float, nullable=False)
    currency = Column(String(10), nullable=False)
    network = Column(String(50), nullable=False)
    period_start = Column(DateTime, nullable=False)
    period_end = Column(DateTime, nullable=False)
    metadata = Column(JSON, nullable=False, default=dict)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    # Relationships
    agent = relationship("Agent", back_populates="revenue_records")
    
    # Indexes
    __table_args__ = (
        Index("idx_revenue_agent_type_period", "agent_id", "revenue_type", "period_start"),
        Index("idx_revenue_created_at", "created_at"),
    )


class CrossChainTransaction(Base):
    """Cross-chain transaction model."""
    __tablename__ = "cross_chain_transactions"
    
    id = Column(String, primary_key=True, index=True)
    source_network = Column(String(50), nullable=False, index=True)
    destination_network = Column(String(50), nullable=False, index=True)
    bridge_type = Column(String(50), nullable=False)
    message_type = Column(String(50), nullable=False)
    status = Column(String(20), nullable=False, default="pending", index=True)
    source_tx_hash = Column(String, nullable=True)
    destination_tx_hash = Column(String, nullable=True)
    amount = Column(Float, nullable=True)
    token_address = Column(String, nullable=True)
    sender_address = Column(String, nullable=False)
    recipient_address = Column(String, nullable=False)
    metadata = Column(JSON, nullable=False, default=dict)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    confirmed_at = Column(DateTime, nullable=True)
    
    # Indexes
    __table_args__ = (
        Index("idx_cross_chain_networks", "source_network", "destination_network"),
        Index("idx_cross_chain_status_created", "status", "created_at"),
        Index("idx_cross_chain_sender", "sender_address"),
    )


class NetworkStatus(Base):
    """Network status model."""
    __tablename__ = "network_status"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    network_name = Column(String(50), nullable=False, index=True)
    network_type = Column(String(50), nullable=False)
    chain_id = Column(Integer, nullable=True)
    block_height = Column(Integer, nullable=False, default=0)
    is_connected = Column(Boolean, nullable=False, default=False)
    gas_price = Column(Float, nullable=True)
    response_time = Column(Float, nullable=True)  # milliseconds
    last_block_time = Column(DateTime, nullable=True)
    error_message = Column(Text, nullable=True)
    metadata = Column(JSON, nullable=False, default=dict)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Indexes
    __table_args__ = (
        Index("idx_network_status_name_updated", "network_name", "updated_at"),
        Index("idx_network_status_connected", "is_connected"),
    )


class AlertRule(Base):
    """Alert rule model."""
    __tablename__ = "alert_rules"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    metric = Column(String(100), nullable=False)
    operator = Column(String(10), nullable=False)  # gt, lt, gte, lte, eq, ne
    threshold = Column(Float, nullable=False)
    duration = Column(Integer, nullable=False, default=300)  # seconds
    severity = Column(String(20), nullable=False, default="warning")
    enabled = Column(Boolean, nullable=False, default=True)
    notification_channels = Column(JSON, nullable=False, default=list)
    agent_id = Column(String, nullable=True)  # Optional: rule for specific agent
    deployment_id = Column(String, nullable=True)  # Optional: rule for specific deployment
    created_by = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Indexes
    __table_args__ = (
        Index("idx_alert_rule_enabled_metric", "enabled", "metric"),
        Index("idx_alert_rule_agent", "agent_id"),
    )


class Alert(Base):
    """Alert model."""
    __tablename__ = "alerts"
    
    id = Column(String, primary_key=True, index=True)
    rule_id = Column(String, ForeignKey("alert_rules.id"), nullable=False)
    agent_id = Column(String, nullable=True)
    deployment_id = Column(String, nullable=True)
    metric = Column(String(100), nullable=False)
    current_value = Column(Float, nullable=False)
    threshold = Column(Float, nullable=False)
    severity = Column(String(20), nullable=False)
    status = Column(String(20), nullable=False, default="active", index=True)  # active, resolved, suppressed
    message = Column(Text, nullable=False)
    metadata = Column(JSON, nullable=False, default=dict)
    fired_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)
    acknowledged_at = Column(DateTime, nullable=True)
    acknowledged_by = Column(String, nullable=True)
    
    # Indexes
    __table_args__ = (
        Index("idx_alert_status_fired", "status", "fired_at"),
        Index("idx_alert_rule_status", "rule_id", "status"),
        Index("idx_alert_severity", "severity"),
    )


async def init_db():
    """Initialize database tables."""
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        
        logger.info("Database tables created successfully")
        
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Get database session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            logger.error(f"Database session error: {e}")
            raise
        finally:
            await session.close()


def get_sync_db() -> Session:
    """Get synchronous database session."""
    db = SyncSessionLocal()
    try:
        return db
    except Exception as e:
        db.rollback()
        logger.error(f"Sync database session error: {e}")
        raise
    finally:
        db.close()
