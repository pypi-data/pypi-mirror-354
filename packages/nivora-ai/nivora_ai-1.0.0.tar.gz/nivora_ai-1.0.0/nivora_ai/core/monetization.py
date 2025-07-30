"""
Monetization framework for Nivora AI SDK.
"""

import asyncio
import uuid
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field

from ..utils.logger import get_logger
from ..utils.exceptions import MonetizationError, BlockchainError

logger = get_logger(__name__)


class PaymentModel(Enum):
    """Payment model enumeration."""
    PAY_PER_USE = "pay_per_use"
    SUBSCRIPTION = "subscription"
    REVENUE_SHARE = "revenue_share"
    TIERED = "tiered"
    FREEMIUM = "freemium"


class PaymentStatus(Enum):
    """Payment status enumeration."""
    PENDING = "pending"
    PROCESSING = "processing"
    CONFIRMED = "confirmed"
    FAILED = "failed"
    REFUNDED = "refunded"


class RevenueType(Enum):
    """Revenue type enumeration."""
    DIRECT_PAYMENT = "direct_payment"
    SUBSCRIPTION_FEE = "subscription_fee"
    REVENUE_SHARE = "revenue_share"
    PLATFORM_FEE = "platform_fee"
    TRANSACTION_FEE = "transaction_fee"


@dataclass
class PaymentConfig:
    """Payment configuration for an agent."""
    agent_id: str
    payment_model: PaymentModel
    base_price: float
    currency: str = "ETH"
    network: str = "ethereum"
    token_address: Optional[str] = None
    revenue_share_percentage: Optional[float] = None
    subscription_duration: Optional[int] = None  # days
    usage_limits: Dict[str, int] = field(default_factory=dict)
    discount_tiers: List[Dict[str, Any]] = field(default_factory=list)
    auto_renewal: bool = False
    enabled: bool = True


@dataclass
class PaymentRecord:
    """Payment record."""
    id: str
    payment_config_id: str
    agent_id: str
    user_address: str
    amount: float
    currency: str
    network: str
    payment_model: PaymentModel
    status: PaymentStatus = PaymentStatus.PENDING
    transaction_hash: Optional[str] = None
    confirmation_blocks: int = 0
    gas_used: Optional[int] = None
    gas_price: Optional[float] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    confirmed_at: Optional[datetime] = None


@dataclass
class RevenueRecord:
    """Revenue record."""
    id: str
    agent_id: str
    revenue_type: RevenueType
    amount: float
    currency: str
    network: str
    period_start: datetime
    period_end: datetime
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)


class MonetizationManager:
    """
    Manages monetization strategies and payment processing for AI agents.
    """
    
    def __init__(self):
        """Initialize monetization manager."""
        self.payment_configs: Dict[str, PaymentConfig] = {}
        self.payment_records: Dict[str, PaymentRecord] = {}
        self.revenue_records: Dict[str, RevenueRecord] = {}
        self.user_subscriptions: Dict[str, Dict[str, Any]] = {}
        self.usage_tracking: Dict[str, Dict[str, Any]] = {}
        self.event_handlers: Dict[str, List[Callable]] = {}
        
    def add_event_handler(self, event: str, handler: Callable) -> None:
        """Add event handler for monetization events."""
        if event not in self.event_handlers:
            self.event_handlers[event] = []
        self.event_handlers[event].append(handler)
    
    def emit_event(self, event: str, data: Dict[str, Any] = None) -> None:
        """Emit event to registered handlers."""
        if event in self.event_handlers:
            for handler in self.event_handlers[event]:
                try:
                    if asyncio.iscoroutinefunction(handler):
                        asyncio.create_task(handler(data or {}))
                    else:
                        handler(data or {})
                except Exception as e:
                    logger.error(f"Error in event handler for {event}: {e}")
    
    async def create_payment_config(self, config: PaymentConfig) -> str:
        """Create payment configuration for an agent."""
        try:
            config_id = str(uuid.uuid4())
            self.payment_configs[config_id] = config
            
            logger.info(f"Payment config created: {config_id} for agent {config.agent_id}")
            
            self.emit_event("payment_config_created", {
                "config_id": config_id,
                "agent_id": config.agent_id,
                "payment_model": config.payment_model.value
            })
            
            return config_id
            
        except Exception as e:
            logger.error(f"Failed to create payment config: {e}")
            raise MonetizationError(f"Payment config creation failed: {e}")
    
    async def process_payment(self, agent_id: str, user_address: str, 
                            amount: float, network: str, 
                            blockchain_manager, metadata: Dict[str, Any] = None) -> str:
        """Process payment for agent usage."""
        try:
            # Find payment config for agent
            config = self._get_agent_payment_config(agent_id)
            if not config:
                raise MonetizationError(f"No payment config found for agent: {agent_id}")
            
            if not config.enabled:
                raise MonetizationError(f"Payments disabled for agent: {agent_id}")
            
            # Validate payment amount
            expected_amount = await self._calculate_payment_amount(
                agent_id, user_address, amount, metadata or {}
            )
            
            if amount < expected_amount:
                raise MonetizationError(f"Insufficient payment amount. Expected: {expected_amount}, Received: {amount}")
            
            # Create payment record
            payment_id = str(uuid.uuid4())
            payment_record = PaymentRecord(
                id=payment_id,
                payment_config_id=config.agent_id,  # Using agent_id as config identifier
                agent_id=agent_id,
                user_address=user_address,
                amount=amount,
                currency=config.currency,
                network=network,
                payment_model=config.payment_model,
                metadata=metadata or {}
            )
            
            self.payment_records[payment_id] = payment_record
            
            # Process blockchain transaction
            network_instance = blockchain_manager.get_network(network)
            if not network_instance:
                raise MonetizationError(f"Network not available: {network}")
            
            # Send payment transaction
            tx_hash = await network_instance.send_transaction(
                to_address=config.token_address or "0x0000000000000000000000000000000000000000",
                amount=amount,
                data=f"Payment for agent {agent_id}"
            )
            
            payment_record.transaction_hash = tx_hash
            payment_record.status = PaymentStatus.PROCESSING
            
            # Start monitoring transaction
            asyncio.create_task(self._monitor_payment(payment_id, blockchain_manager))
            
            logger.info(f"Payment processed: {payment_id} for agent {agent_id}")
            
            self.emit_event("payment_processed", {
                "payment_id": payment_id,
                "agent_id": agent_id,
                "user_address": user_address,
                "amount": amount,
                "tx_hash": tx_hash
            })
            
            return payment_id
            
        except Exception as e:
            logger.error(f"Payment processing failed: {e}")
            raise MonetizationError(f"Payment processing failed: {e}")
    
    async def _monitor_payment(self, payment_id: str, blockchain_manager) -> None:
        """Monitor payment transaction confirmation."""
        try:
            payment = self.payment_records.get(payment_id)
            if not payment or not payment.transaction_hash:
                return
            
            network_instance = blockchain_manager.get_network(payment.network)
            if not network_instance:
                return
            
            # Wait for transaction confirmation
            for _ in range(60):  # Wait up to 10 minutes
                try:
                    tx_status = await network_instance.get_transaction_status(payment.transaction_hash)
                    
                    if tx_status.get("confirmed", False):
                        payment.status = PaymentStatus.CONFIRMED
                        payment.confirmed_at = datetime.utcnow()
                        payment.confirmation_blocks = tx_status.get("confirmations", 0)
                        payment.gas_used = tx_status.get("gas_used")
                        payment.gas_price = tx_status.get("gas_price")
                        
                        # Update usage tracking
                        await self._update_usage_tracking(payment)
                        
                        # Record revenue
                        await self._record_revenue(payment)
                        
                        self.emit_event("payment_confirmed", {
                            "payment_id": payment_id,
                            "agent_id": payment.agent_id,
                            "amount": payment.amount
                        })
                        
                        logger.info(f"Payment confirmed: {payment_id}")
                        break
                    elif tx_status.get("failed", False):
                        payment.status = PaymentStatus.FAILED
                        
                        self.emit_event("payment_failed", {
                            "payment_id": payment_id,
                            "agent_id": payment.agent_id,
                            "error": "Transaction failed"
                        })
                        
                        logger.error(f"Payment failed: {payment_id}")
                        break
                        
                except Exception as e:
                    logger.error(f"Error monitoring payment {payment_id}: {e}")
                
                await asyncio.sleep(10)  # Check every 10 seconds
                
        except Exception as e:
            logger.error(f"Payment monitoring error: {e}")
    
    async def _calculate_payment_amount(self, agent_id: str, user_address: str, 
                                      requested_amount: float, metadata: Dict[str, Any]) -> float:
        """Calculate required payment amount based on configuration."""
        config = self._get_agent_payment_config(agent_id)
        if not config:
            return requested_amount
        
        base_amount = config.base_price
        
        # Apply payment model specific calculations
        if config.payment_model == PaymentModel.PAY_PER_USE:
            usage_count = metadata.get("usage_count", 1)
            base_amount = config.base_price * usage_count
            
        elif config.payment_model == PaymentModel.SUBSCRIPTION:
            # Subscription amount is fixed
            base_amount = config.base_price
            
        elif config.payment_model == PaymentModel.TIERED:
            # Apply tiered pricing
            usage_level = metadata.get("usage_level", "basic")
            for tier in config.discount_tiers:
                if tier.get("level") == usage_level:
                    base_amount = tier.get("price", config.base_price)
                    break
        
        # Apply discounts
        discount_percentage = self._calculate_discount(user_address, config)
        if discount_percentage > 0:
            base_amount = base_amount * (1 - discount_percentage / 100)
        
        return base_amount
    
    def _calculate_discount(self, user_address: str, config: PaymentConfig) -> float:
        """Calculate discount percentage for user."""
        # Check if user has existing subscriptions (loyalty discount)
        user_payments = [
            payment for payment in self.payment_records.values()
            if payment.user_address == user_address and payment.status == PaymentStatus.CONFIRMED
        ]
        
        payment_count = len(user_payments)
        
        # Apply volume discounts based on discount tiers
        for tier in config.discount_tiers:
            min_payments = tier.get("min_payments", 0)
            if payment_count >= min_payments:
                return tier.get("discount_percentage", 0)
        
        return 0
    
    async def _update_usage_tracking(self, payment: PaymentRecord) -> None:
        """Update usage tracking for user."""
        user_key = f"{payment.user_address}_{payment.agent_id}"
        
        if user_key not in self.usage_tracking:
            self.usage_tracking[user_key] = {
                "user_address": payment.user_address,
                "agent_id": payment.agent_id,
                "total_payments": 0,
                "total_amount": 0,
                "last_payment": None,
                "usage_count": 0
            }
        
        tracking = self.usage_tracking[user_key]
        tracking["total_payments"] += 1
        tracking["total_amount"] += payment.amount
        tracking["last_payment"] = payment.created_at
        tracking["usage_count"] += payment.metadata.get("usage_count", 1)
    
    async def _record_revenue(self, payment: PaymentRecord) -> None:
        """Record revenue from payment."""
        try:
            revenue_id = str(uuid.uuid4())
            
            # Calculate platform fee (e.g., 2.5%)
            platform_fee_percentage = 2.5
            platform_fee = payment.amount * (platform_fee_percentage / 100)
            agent_revenue = payment.amount - platform_fee
            
            # Record agent revenue
            agent_revenue_record = RevenueRecord(
                id=revenue_id,
                agent_id=payment.agent_id,
                revenue_type=RevenueType.DIRECT_PAYMENT,
                amount=agent_revenue,
                currency=payment.currency,
                network=payment.network,
                period_start=payment.created_at,
                period_end=payment.created_at,
                metadata={
                    "payment_id": payment.id,
                    "original_amount": payment.amount,
                    "platform_fee": platform_fee
                }
            )
            
            self.revenue_records[revenue_id] = agent_revenue_record
            
            # Record platform fee
            platform_revenue_id = str(uuid.uuid4())
            platform_revenue_record = RevenueRecord(
                id=platform_revenue_id,
                agent_id="platform",
                revenue_type=RevenueType.PLATFORM_FEE,
                amount=platform_fee,
                currency=payment.currency,
                network=payment.network,
                period_start=payment.created_at,
                period_end=payment.created_at,
                metadata={
                    "payment_id": payment.id,
                    "agent_id": payment.agent_id
                }
            )
            
            self.revenue_records[platform_revenue_id] = platform_revenue_record
            
            logger.info(f"Revenue recorded: Agent {agent_revenue}, Platform {platform_fee}")
            
        except Exception as e:
            logger.error(f"Failed to record revenue: {e}")
    
    async def create_subscription(self, agent_id: str, user_address: str, 
                                duration_days: int, blockchain_manager) -> str:
        """Create subscription for user."""
        try:
            config = self._get_agent_payment_config(agent_id)
            if not config:
                raise MonetizationError(f"No payment config found for agent: {agent_id}")
            
            if config.payment_model != PaymentModel.SUBSCRIPTION:
                raise MonetizationError(f"Agent {agent_id} does not support subscriptions")
            
            # Process subscription payment
            payment_id = await self.process_payment(
                agent_id=agent_id,
                user_address=user_address,
                amount=config.base_price,
                network=config.network,
                blockchain_manager=blockchain_manager,
                metadata={"subscription_duration": duration_days}
            )
            
            # Create subscription record
            subscription_id = str(uuid.uuid4())
            subscription = {
                "id": subscription_id,
                "agent_id": agent_id,
                "user_address": user_address,
                "payment_id": payment_id,
                "start_date": datetime.utcnow(),
                "end_date": datetime.utcnow() + timedelta(days=duration_days),
                "auto_renewal": config.auto_renewal,
                "status": "active",
                "created_at": datetime.utcnow()
            }
            
            user_key = f"{user_address}_{agent_id}"
            self.user_subscriptions[user_key] = subscription
            
            logger.info(f"Subscription created: {subscription_id}")
            
            self.emit_event("subscription_created", {
                "subscription_id": subscription_id,
                "agent_id": agent_id,
                "user_address": user_address,
                "duration_days": duration_days
            })
            
            return subscription_id
            
        except Exception as e:
            logger.error(f"Subscription creation failed: {e}")
            raise MonetizationError(f"Subscription creation failed: {e}")
    
    def check_access_permission(self, agent_id: str, user_address: str) -> bool:
        """Check if user has permission to access agent."""
        config = self._get_agent_payment_config(agent_id)
        if not config:
            return False  # No config means no access
        
        if config.payment_model == PaymentModel.FREEMIUM:
            # Check usage limits for freemium
            return self._check_freemium_limits(agent_id, user_address)
        elif config.payment_model == PaymentModel.SUBSCRIPTION:
            # Check active subscription
            return self._check_subscription_status(agent_id, user_address)
        else:
            # For pay-per-use, always allow (payment happens during usage)
            return True
    
    def _check_freemium_limits(self, agent_id: str, user_address: str) -> bool:
        """Check freemium usage limits."""
        config = self._get_agent_payment_config(agent_id)
        if not config:
            return False
        
        user_key = f"{user_address}_{agent_id}"
        tracking = self.usage_tracking.get(user_key, {})
        
        current_usage = tracking.get("usage_count", 0)
        limit = config.usage_limits.get("monthly_requests", 100)
        
        # Check if within current month
        last_payment = tracking.get("last_payment")
        if last_payment:
            days_since_last = (datetime.utcnow() - last_payment).days
            if days_since_last > 30:
                # Reset monthly usage
                tracking["usage_count"] = 0
                current_usage = 0
        
        return current_usage < limit
    
    def _check_subscription_status(self, agent_id: str, user_address: str) -> bool:
        """Check subscription status."""
        user_key = f"{user_address}_{agent_id}"
        subscription = self.user_subscriptions.get(user_key)
        
        if not subscription:
            return False
        
        if subscription["status"] != "active":
            return False
        
        # Check if subscription is still valid
        if datetime.utcnow() > subscription["end_date"]:
            subscription["status"] = "expired"
            return False
        
        return True
    
    def _get_agent_payment_config(self, agent_id: str) -> Optional[PaymentConfig]:
        """Get payment configuration for agent."""
        for config in self.payment_configs.values():
            if config.agent_id == agent_id:
                return config
        return None
    
    def get_revenue_analytics(self, agent_id: Optional[str] = None, 
                            start_date: Optional[datetime] = None,
                            end_date: Optional[datetime] = None) -> Dict[str, Any]:
        """Get revenue analytics."""
        revenues = list(self.revenue_records.values())
        
        # Filter by agent
        if agent_id:
            revenues = [r for r in revenues if r.agent_id == agent_id]
        
        # Filter by date range
        if start_date:
            revenues = [r for r in revenues if r.created_at >= start_date]
        if end_date:
            revenues = [r for r in revenues if r.created_at <= end_date]
        
        # Calculate analytics
        total_revenue = sum(r.amount for r in revenues)
        revenue_by_type = {}
        revenue_by_currency = {}
        
        for revenue in revenues:
            # Group by revenue type
            revenue_type = revenue.revenue_type.value
            if revenue_type not in revenue_by_type:
                revenue_by_type[revenue_type] = 0
            revenue_by_type[revenue_type] += revenue.amount
            
            # Group by currency
            if revenue.currency not in revenue_by_currency:
                revenue_by_currency[revenue.currency] = 0
            revenue_by_currency[revenue.currency] += revenue.amount
        
        return {
            "total_revenue": total_revenue,
            "revenue_count": len(revenues),
            "revenue_by_type": revenue_by_type,
            "revenue_by_currency": revenue_by_currency,
            "period_start": start_date,
            "period_end": end_date
        }
    
    def get_payment_status(self, payment_id: str) -> Optional[Dict[str, Any]]:
        """Get payment status."""
        payment = self.payment_records.get(payment_id)
        if not payment:
            return None
        
        return {
            "payment_id": payment.id,
            "agent_id": payment.agent_id,
            "user_address": payment.user_address,
            "amount": payment.amount,
            "currency": payment.currency,
            "status": payment.status.value,
            "transaction_hash": payment.transaction_hash,
            "created_at": payment.created_at,
            "confirmed_at": payment.confirmed_at
        }
    
    def get_user_usage_stats(self, user_address: str) -> Dict[str, Any]:
        """Get usage statistics for user."""
        user_stats = {}
        
        for key, tracking in self.usage_tracking.items():
            if tracking["user_address"] == user_address:
                agent_id = tracking["agent_id"]
                user_stats[agent_id] = {
                    "total_payments": tracking["total_payments"],
                    "total_amount": tracking["total_amount"],
                    "usage_count": tracking["usage_count"],
                    "last_payment": tracking["last_payment"]
                }
        
        return user_stats