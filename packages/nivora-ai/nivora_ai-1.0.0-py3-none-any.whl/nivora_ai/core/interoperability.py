"""
Cross-chain interoperability for Nivora AI SDK.
"""

import asyncio
import uuid
from datetime import datetime
from enum import Enum
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field

from ..utils.logger import get_logger
from ..utils.exceptions import NetworkError, BlockchainError

logger = get_logger(__name__)


class BridgeType(Enum):
    """Bridge type enumeration."""
    CANONICAL = "canonical"
    LOCK_AND_MINT = "lock_and_mint"
    BURN_AND_MINT = "burn_and_mint"
    LIQUIDITY_POOL = "liquidity_pool"
    ROLLUP = "rollup"


class MessageType(Enum):
    """Cross-chain message type enumeration."""
    TOKEN_TRANSFER = "token_transfer"
    CONTRACT_CALL = "contract_call"
    DATA_SYNC = "data_sync"
    AGENT_COMMAND = "agent_command"
    PAYMENT_SETTLEMENT = "payment_settlement"


class CrossChainStatus(Enum):
    """Cross-chain transaction status."""
    PENDING = "pending"
    INITIATED = "initiated"
    CONFIRMED_SOURCE = "confirmed_source"
    BRIDGING = "bridging"
    CONFIRMED_DESTINATION = "confirmed_destination"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class CrossChainMessage:
    """Cross-chain message structure."""
    id: str
    source_network: str
    destination_network: str
    bridge_type: BridgeType
    message_type: MessageType
    payload: Dict[str, Any]
    sender_address: str
    recipient_address: str
    amount: Optional[float] = None
    token_address: Optional[str] = None
    gas_limit: Optional[int] = None
    deadline: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CrossChainTransaction:
    """Cross-chain transaction record."""
    id: str
    message: CrossChainMessage
    status: CrossChainStatus = CrossChainStatus.PENDING
    source_tx_hash: Optional[str] = None
    destination_tx_hash: Optional[str] = None
    bridge_tx_hash: Optional[str] = None
    error_message: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    initiated_at: Optional[datetime] = None
    confirmed_at: Optional[datetime] = None


class CrossChainManager:
    """
    Manages cross-chain operations and interoperability between different blockchain networks.
    """
    
    def __init__(self):
        """Initialize cross-chain manager."""
        self.transactions: Dict[str, CrossChainTransaction] = {}
        self.bridge_configs: Dict[str, Dict[str, Any]] = {}
        self.network_mappings: Dict[str, Dict[str, str]] = {}
        self.event_handlers: Dict[str, List[Callable]] = {}
        self.supported_bridges: List[BridgeType] = [
            BridgeType.CANONICAL,
            BridgeType.LOCK_AND_MINT,
            BridgeType.BURN_AND_MINT
        ]
        
        # Initialize default bridge configurations
        self._init_default_bridges()
    
    def _init_default_bridges(self) -> None:
        """Initialize default bridge configurations."""
        # Ethereum <-> Polygon bridge
        self.bridge_configs["ethereum_polygon"] = {
            "bridge_type": BridgeType.CANONICAL,
            "contract_address": "0x8484Ef722627bf18ca5Ae6BcF031c23E6e922B30",
            "min_amount": 0.01,
            "max_amount": 1000,
            "fee_percentage": 0.1,
            "confirmation_blocks": 12
        }
        
        # Ethereum <-> BSC bridge
        self.bridge_configs["ethereum_bsc"] = {
            "bridge_type": BridgeType.LOCK_AND_MINT,
            "contract_address": "0x3ee18B2214AFF97000D974cf647E7C347E8fa585",
            "min_amount": 0.01,
            "max_amount": 500,
            "fee_percentage": 0.2,
            "confirmation_blocks": 15
        }
        
        # Polygon <-> BSC bridge
        self.bridge_configs["polygon_bsc"] = {
            "bridge_type": BridgeType.BURN_AND_MINT,
            "contract_address": "0x2953399124F0cBB46d2CbACD8A89cF0599974963",
            "min_amount": 1,
            "max_amount": 10000,
            "fee_percentage": 0.15,
            "confirmation_blocks": 10
        }
    
    def add_event_handler(self, event: str, handler: Callable) -> None:
        """Add event handler for cross-chain events."""
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
    
    async def send_cross_chain_message(self, message: CrossChainMessage, 
                                     blockchain_manager) -> str:
        """Send a cross-chain message."""
        try:
            # Validate message
            await self._validate_message(message)
            
            # Create transaction record
            tx_id = str(uuid.uuid4())
            transaction = CrossChainTransaction(
                id=tx_id,
                message=message
            )
            
            self.transactions[tx_id] = transaction
            
            # Get bridge configuration
            bridge_key = f"{message.source_network}_{message.destination_network}"
            bridge_config = self.bridge_configs.get(bridge_key)
            
            if not bridge_config:
                raise NetworkError(f"No bridge configured for {message.source_network} -> {message.destination_network}")
            
            # Initiate cross-chain transaction
            await self._initiate_cross_chain_tx(transaction, bridge_config, blockchain_manager)
            
            # Start monitoring
            asyncio.create_task(self._monitor_cross_chain_tx(tx_id, blockchain_manager))
            
            logger.info(f"Cross-chain message initiated: {tx_id}")
            
            self.emit_event("cross_chain_initiated", {
                "transaction_id": tx_id,
                "source_network": message.source_network,
                "destination_network": message.destination_network,
                "message_type": message.message_type.value
            })
            
            return tx_id
            
        except Exception as e:
            logger.error(f"Failed to send cross-chain message: {e}")
            raise NetworkError(f"Cross-chain message failed: {e}")
    
    async def _validate_message(self, message: CrossChainMessage) -> None:
        """Validate cross-chain message."""
        if message.source_network == message.destination_network:
            raise ValueError("Source and destination networks cannot be the same")
        
        if message.amount is not None and message.amount <= 0:
            raise ValueError("Amount must be positive")
        
        # Validate bridge configuration exists
        bridge_key = f"{message.source_network}_{message.destination_network}"
        if bridge_key not in self.bridge_configs:
            raise ValueError(f"No bridge configured for {message.source_network} -> {message.destination_network}")
        
        bridge_config = self.bridge_configs[bridge_key]
        
        # Validate amount limits
        if message.amount:
            if message.amount < bridge_config["min_amount"]:
                raise ValueError(f"Amount below minimum: {bridge_config['min_amount']}")
            if message.amount > bridge_config["max_amount"]:
                raise ValueError(f"Amount above maximum: {bridge_config['max_amount']}")
    
    async def _initiate_cross_chain_tx(self, transaction: CrossChainTransaction, 
                                     bridge_config: Dict[str, Any], 
                                     blockchain_manager) -> None:
        """Initiate cross-chain transaction on source network."""
        try:
            message = transaction.message
            source_network = blockchain_manager.get_network(message.source_network)
            
            if not source_network:
                raise NetworkError(f"Source network not available: {message.source_network}")
            
            # Prepare transaction data based on bridge type
            tx_data = await self._prepare_bridge_transaction(message, bridge_config)
            
            # Send transaction on source network
            tx_hash = await source_network.send_transaction(
                to_address=bridge_config["contract_address"],
                amount=message.amount or 0,
                data=tx_data
            )
            
            transaction.source_tx_hash = tx_hash
            transaction.status = CrossChainStatus.INITIATED
            transaction.initiated_at = datetime.utcnow()
            
            logger.info(f"Cross-chain transaction initiated: {tx_hash}")
            
        except Exception as e:
            transaction.status = CrossChainStatus.FAILED
            transaction.error_message = str(e)
            logger.error(f"Failed to initiate cross-chain transaction: {e}")
            raise
    
    async def _prepare_bridge_transaction(self, message: CrossChainMessage, 
                                        bridge_config: Dict[str, Any]) -> str:
        """Prepare bridge transaction data."""
        bridge_type = bridge_config["bridge_type"]
        
        if bridge_type == BridgeType.CANONICAL:
            return self._prepare_canonical_bridge_data(message)
        elif bridge_type == BridgeType.LOCK_AND_MINT:
            return self._prepare_lock_mint_data(message)
        elif bridge_type == BridgeType.BURN_AND_MINT:
            return self._prepare_burn_mint_data(message)
        else:
            raise ValueError(f"Unsupported bridge type: {bridge_type}")
    
    def _prepare_canonical_bridge_data(self, message: CrossChainMessage) -> str:
        """Prepare data for canonical bridge."""
        # Simplified bridge data encoding
        data = {
            "recipient": message.recipient_address,
            "amount": message.amount or 0,
            "destination_chain": message.destination_network,
            "message_type": message.message_type.value,
            "payload": message.payload
        }
        return str(data)  # In real implementation, this would be ABI encoded
    
    def _prepare_lock_mint_data(self, message: CrossChainMessage) -> str:
        """Prepare data for lock-and-mint bridge."""
        data = {
            "lock_recipient": message.recipient_address,
            "lock_amount": message.amount or 0,
            "mint_chain": message.destination_network,
            "token_address": message.token_address,
            "payload": message.payload
        }
        return str(data)
    
    def _prepare_burn_mint_data(self, message: CrossChainMessage) -> str:
        """Prepare data for burn-and-mint bridge."""
        data = {
            "burn_amount": message.amount or 0,
            "mint_recipient": message.recipient_address,
            "mint_chain": message.destination_network,
            "token_address": message.token_address,
            "payload": message.payload
        }
        return str(data)
    
    async def _monitor_cross_chain_tx(self, tx_id: str, blockchain_manager) -> None:
        """Monitor cross-chain transaction progress."""
        try:
            transaction = self.transactions.get(tx_id)
            if not transaction:
                return
            
            message = transaction.message
            source_network = blockchain_manager.get_network(message.source_network)
            destination_network = blockchain_manager.get_network(message.destination_network)
            
            # Monitor source transaction
            await self._monitor_source_confirmation(transaction, source_network)
            
            if transaction.status == CrossChainStatus.FAILED:
                return
            
            # Simulate bridging process (in real implementation, this would interact with actual bridges)
            await self._simulate_bridging_process(transaction)
            
            # Monitor destination transaction
            await self._monitor_destination_confirmation(transaction, destination_network)
            
        except Exception as e:
            if tx_id in self.transactions:
                self.transactions[tx_id].status = CrossChainStatus.FAILED
                self.transactions[tx_id].error_message = str(e)
            logger.error(f"Cross-chain monitoring error: {e}")
    
    async def _monitor_source_confirmation(self, transaction: CrossChainTransaction, 
                                         source_network) -> None:
        """Monitor source transaction confirmation."""
        if not transaction.source_tx_hash or not source_network:
            return
        
        # Wait for confirmation
        for _ in range(30):  # Wait up to 5 minutes
            try:
                tx_status = await source_network.get_transaction_status(transaction.source_tx_hash)
                
                if tx_status.get("confirmed", False):
                    transaction.status = CrossChainStatus.CONFIRMED_SOURCE
                    
                    self.emit_event("cross_chain_source_confirmed", {
                        "transaction_id": transaction.id,
                        "source_tx_hash": transaction.source_tx_hash
                    })
                    
                    logger.info(f"Source transaction confirmed: {transaction.source_tx_hash}")
                    break
                elif tx_status.get("failed", False):
                    transaction.status = CrossChainStatus.FAILED
                    transaction.error_message = "Source transaction failed"
                    break
                    
            except Exception as e:
                logger.error(f"Error monitoring source transaction: {e}")
            
            await asyncio.sleep(10)
    
    async def _simulate_bridging_process(self, transaction: CrossChainTransaction) -> None:
        """Simulate bridging process (placeholder for actual bridge integration)."""
        if transaction.status != CrossChainStatus.CONFIRMED_SOURCE:
            return
        
        # Simulate bridge processing time
        await asyncio.sleep(30)  # 30 seconds simulation
        
        transaction.status = CrossChainStatus.BRIDGING
        transaction.bridge_tx_hash = f"bridge_{uuid.uuid4()}"
        
        self.emit_event("cross_chain_bridging", {
            "transaction_id": transaction.id,
            "bridge_tx_hash": transaction.bridge_tx_hash
        })
        
        logger.info(f"Cross-chain bridging started: {transaction.bridge_tx_hash}")
    
    async def _monitor_destination_confirmation(self, transaction: CrossChainTransaction, 
                                              destination_network) -> None:
        """Monitor destination transaction confirmation."""
        if transaction.status != CrossChainStatus.BRIDGING:
            return
        
        # Simulate destination transaction
        await asyncio.sleep(20)  # Simulate processing time
        
        transaction.destination_tx_hash = f"dest_{uuid.uuid4()}"
        transaction.status = CrossChainStatus.CONFIRMED_DESTINATION
        
        # Final completion
        await asyncio.sleep(10)
        transaction.status = CrossChainStatus.COMPLETED
        transaction.confirmed_at = datetime.utcnow()
        
        self.emit_event("cross_chain_completed", {
            "transaction_id": transaction.id,
            "destination_tx_hash": transaction.destination_tx_hash
        })
        
        logger.info(f"Cross-chain transaction completed: {transaction.id}")
    
    async def transfer_tokens(self, source_network: str, destination_network: str,
                            token_address: str, amount: float, 
                            sender_address: str, recipient_address: str,
                            blockchain_manager) -> str:
        """Transfer tokens across chains."""
        message = CrossChainMessage(
            id=str(uuid.uuid4()),
            source_network=source_network,
            destination_network=destination_network,
            bridge_type=BridgeType.LOCK_AND_MINT,
            message_type=MessageType.TOKEN_TRANSFER,
            payload={"token_transfer": True},
            sender_address=sender_address,
            recipient_address=recipient_address,
            amount=amount,
            token_address=token_address
        )
        
        return await self.send_cross_chain_message(message, blockchain_manager)
    
    async def sync_agent_data(self, source_network: str, destination_network: str,
                            agent_id: str, data: Dict[str, Any],
                            sender_address: str, blockchain_manager) -> str:
        """Synchronize agent data across chains."""
        message = CrossChainMessage(
            id=str(uuid.uuid4()),
            source_network=source_network,
            destination_network=destination_network,
            bridge_type=BridgeType.CANONICAL,
            message_type=MessageType.DATA_SYNC,
            payload={
                "agent_id": agent_id,
                "data": data,
                "sync_type": "agent_data"
            },
            sender_address=sender_address,
            recipient_address=sender_address  # Same address on destination
        )
        
        return await self.send_cross_chain_message(message, blockchain_manager)
    
    async def execute_cross_chain_agent_command(self, source_network: str, destination_network: str,
                                              agent_id: str, command: str, parameters: Dict[str, Any],
                                              sender_address: str, blockchain_manager) -> str:
        """Execute agent command across chains."""
        message = CrossChainMessage(
            id=str(uuid.uuid4()),
            source_network=source_network,
            destination_network=destination_network,
            bridge_type=BridgeType.CANONICAL,
            message_type=MessageType.AGENT_COMMAND,
            payload={
                "agent_id": agent_id,
                "command": command,
                "parameters": parameters
            },
            sender_address=sender_address,
            recipient_address=sender_address
        )
        
        return await self.send_cross_chain_message(message, blockchain_manager)
    
    def get_transaction_status(self, tx_id: str) -> Optional[Dict[str, Any]]:
        """Get cross-chain transaction status."""
        transaction = self.transactions.get(tx_id)
        if not transaction:
            return None
        
        return {
            "transaction_id": transaction.id,
            "status": transaction.status.value,
            "source_network": transaction.message.source_network,
            "destination_network": transaction.message.destination_network,
            "message_type": transaction.message.message_type.value,
            "amount": transaction.message.amount,
            "source_tx_hash": transaction.source_tx_hash,
            "destination_tx_hash": transaction.destination_tx_hash,
            "bridge_tx_hash": transaction.bridge_tx_hash,
            "error_message": transaction.error_message,
            "created_at": transaction.created_at,
            "confirmed_at": transaction.confirmed_at
        }
    
    def get_bridge_info(self, source_network: str, destination_network: str) -> Optional[Dict[str, Any]]:
        """Get bridge information between networks."""
        bridge_key = f"{source_network}_{destination_network}"
        bridge_config = self.bridge_configs.get(bridge_key)
        
        if not bridge_config:
            return None
        
        return {
            "source_network": source_network,
            "destination_network": destination_network,
            "bridge_type": bridge_config["bridge_type"].value if isinstance(bridge_config["bridge_type"], BridgeType) else bridge_config["bridge_type"],
            "contract_address": bridge_config["contract_address"],
            "min_amount": bridge_config["min_amount"],
            "max_amount": bridge_config["max_amount"],
            "fee_percentage": bridge_config["fee_percentage"],
            "confirmation_blocks": bridge_config["confirmation_blocks"]
        }
    
    def get_supported_routes(self) -> List[Dict[str, str]]:
        """Get all supported cross-chain routes."""
        routes = []
        for bridge_key in self.bridge_configs.keys():
            source, destination = bridge_key.split("_", 1)
            routes.append({
                "source_network": source,
                "destination_network": destination
            })
            # Add reverse route if not explicitly configured
            reverse_key = f"{destination}_{source}"
            if reverse_key not in self.bridge_configs:
                routes.append({
                    "source_network": destination,
                    "destination_network": source
                })
        return routes
    
    def get_all_transactions(self) -> Dict[str, Dict[str, Any]]:
        """Get all cross-chain transactions."""
        return {
            tx_id: self.get_transaction_status(tx_id)
            for tx_id in self.transactions.keys()
        }