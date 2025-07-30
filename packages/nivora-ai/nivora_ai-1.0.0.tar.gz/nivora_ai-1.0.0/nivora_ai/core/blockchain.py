"""
Blockchain management and abstraction layer for Nivora AI SDK.
"""

import asyncio
from typing import Dict, Any, Optional, List, Union
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum

from ..utils.logger import get_logger
from ..utils.exceptions import BlockchainException, NetworkException
from ..networks.ethereum import EthereumNetwork
from ..networks.polygon import PolygonNetwork
from ..networks.bsc import BSCNetwork
from ..networks.solana import SolanaNetwork

logger = get_logger(__name__)


class NetworkType(Enum):
    """Supported blockchain networks."""
    ETHEREUM = "ethereum"
    POLYGON = "polygon"
    BSC = "bsc"
    SOLANA = "solana"


@dataclass
class NetworkConfig:
    """Network configuration."""
    network_type: NetworkType
    rpc_url: str
    chain_id: Optional[int] = None
    gas_price: Optional[int] = None
    gas_limit: Optional[int] = None
    private_key: Optional[str] = None
    custom_params: Dict[str, Any] = None

    def __post_init__(self):
        if self.custom_params is None:
            self.custom_params = {}


class BaseBlockchainNetwork(ABC):
    """Abstract base class for blockchain network implementations."""
    
    def __init__(self, config: NetworkConfig):
        self.config = config
        self.network_type = config.network_type
        self.is_connected = False
        self.block_height = 0
        
    @abstractmethod
    async def connect(self) -> bool:
        """Connect to the blockchain network."""
        pass
    
    @abstractmethod
    async def disconnect(self) -> None:
        """Disconnect from the blockchain network."""
        pass
    
    @abstractmethod
    async def deploy_contract(self, contract_code: str, constructor_args: List[Any] = None) -> str:
        """Deploy a smart contract."""
        pass
    
    @abstractmethod
    async def call_contract(self, contract_address: str, method_name: str, args: List[Any] = None) -> Any:
        """Call a smart contract method."""
        pass
    
    @abstractmethod
    async def send_transaction(self, to_address: str, amount: float, data: str = None) -> str:
        """Send a transaction."""
        pass
    
    @abstractmethod
    async def get_balance(self, address: str) -> float:
        """Get account balance."""
        pass
    
    @abstractmethod
    async def get_transaction_status(self, tx_hash: str) -> Dict[str, Any]:
        """Get transaction status."""
        pass
    
    @abstractmethod
    async def estimate_gas(self, transaction: Dict[str, Any]) -> int:
        """Estimate gas for transaction."""
        pass


class BlockchainManager:
    """
    Central manager for handling multiple blockchain networks.
    """
    
    def __init__(self):
        """Initialize blockchain manager."""
        self.networks: Dict[str, BaseBlockchainNetwork] = {}
        self.network_configs: Dict[str, NetworkConfig] = {}
        self.active_networks: List[str] = []
        
        # Network class mapping
        self.network_classes = {
            NetworkType.ETHEREUM: EthereumNetwork,
            NetworkType.POLYGON: PolygonNetwork,
            NetworkType.BSC: BSCNetwork,
            NetworkType.SOLANA: SolanaNetwork,
        }
        
        logger.info("Initialized BlockchainManager")
    
    async def add_network(self, network_name: str, config: NetworkConfig) -> None:
        """Add a blockchain network to the manager."""
        try:
            network_class = self.network_classes.get(config.network_type)
            if not network_class:
                raise NetworkException(f"Unsupported network type: {config.network_type}")
            
            network = network_class(config)
            self.networks[network_name] = network
            self.network_configs[network_name] = config
            
            logger.info(f"Added network '{network_name}' of type {config.network_type.value}")
            
        except Exception as e:
            raise BlockchainException(f"Failed to add network '{network_name}': {e}")
    
    async def connect_network(self, network_name: str) -> bool:
        """Connect to a specific blockchain network."""
        if network_name not in self.networks:
            raise NetworkException(f"Network '{network_name}' not found")
        
        try:
            network = self.networks[network_name]
            success = await network.connect()
            
            if success and network_name not in self.active_networks:
                self.active_networks.append(network_name)
                logger.info(f"Successfully connected to network '{network_name}'")
            
            return success
            
        except Exception as e:
            raise BlockchainException(f"Failed to connect to network '{network_name}': {e}")
    
    async def disconnect_network(self, network_name: str) -> None:
        """Disconnect from a specific blockchain network."""
        if network_name not in self.networks:
            raise NetworkException(f"Network '{network_name}' not found")
        
        try:
            network = self.networks[network_name]
            await network.disconnect()
            
            if network_name in self.active_networks:
                self.active_networks.remove(network_name)
                logger.info(f"Disconnected from network '{network_name}'")
                
        except Exception as e:
            raise BlockchainException(f"Failed to disconnect from network '{network_name}': {e}")
    
    async def connect_all_networks(self) -> Dict[str, bool]:
        """Connect to all configured networks."""
        results = {}
        
        for network_name in self.networks.keys():
            try:
                results[network_name] = await self.connect_network(network_name)
            except Exception as e:
                results[network_name] = False
                logger.error(f"Failed to connect to network '{network_name}': {e}")
        
        return results
    
    async def disconnect_all_networks(self) -> None:
        """Disconnect from all networks."""
        for network_name in list(self.active_networks):
            try:
                await self.disconnect_network(network_name)
            except Exception as e:
                logger.error(f"Failed to disconnect from network '{network_name}': {e}")
    
    def get_network(self, network_name: str) -> BaseBlockchainNetwork:
        """Get a specific network instance."""
        if network_name not in self.networks:
            raise NetworkException(f"Network '{network_name}' not found")
        
        return self.networks[network_name]
    
    def get_active_networks(self) -> List[str]:
        """Get list of active network names."""
        return self.active_networks.copy()
    
    async def deploy_to_network(self, network_name: str, contract_code: str, 
                              constructor_args: List[Any] = None) -> str:
        """Deploy contract to a specific network."""
        network = self.get_network(network_name)
        
        if not network.is_connected:
            await self.connect_network(network_name)
        
        return await network.deploy_contract(contract_code, constructor_args)
    
    async def deploy_to_multiple_networks(self, network_names: List[str], 
                                        contract_code: str, 
                                        constructor_args: List[Any] = None) -> Dict[str, str]:
        """Deploy contract to multiple networks."""
        deployment_results = {}
        
        for network_name in network_names:
            try:
                contract_address = await self.deploy_to_network(
                    network_name, contract_code, constructor_args
                )
                deployment_results[network_name] = contract_address
                logger.info(f"Successfully deployed to {network_name}: {contract_address}")
                
            except Exception as e:
                deployment_results[network_name] = None
                logger.error(f"Failed to deploy to {network_name}: {e}")
        
        return deployment_results
    
    async def call_contract_on_network(self, network_name: str, contract_address: str,
                                     method_name: str, args: List[Any] = None) -> Any:
        """Call contract method on a specific network."""
        network = self.get_network(network_name)
        
        if not network.is_connected:
            await self.connect_network(network_name)
        
        return await network.call_contract(contract_address, method_name, args)
    
    async def send_cross_chain_transaction(self, transactions: Dict[str, Dict[str, Any]]) -> Dict[str, str]:
        """Send transactions across multiple networks."""
        results = {}
        
        for network_name, tx_data in transactions.items():
            try:
                network = self.get_network(network_name)
                
                if not network.is_connected:
                    await self.connect_network(network_name)
                
                tx_hash = await network.send_transaction(
                    tx_data["to_address"],
                    tx_data["amount"],
                    tx_data.get("data")
                )
                
                results[network_name] = tx_hash
                logger.info(f"Cross-chain transaction sent on {network_name}: {tx_hash}")
                
            except Exception as e:
                results[network_name] = None
                logger.error(f"Failed to send transaction on {network_name}: {e}")
        
        return results
    
    async def get_network_status(self, network_name: str) -> Dict[str, Any]:
        """Get status information for a specific network."""
        if network_name not in self.networks:
            raise NetworkException(f"Network '{network_name}' not found")
        
        network = self.networks[network_name]
        config = self.network_configs[network_name]
        
        return {
            "name": network_name,
            "type": config.network_type.value,
            "connected": network.is_connected,
            "block_height": network.block_height,
            "rpc_url": config.rpc_url,
            "chain_id": config.chain_id,
        }
    
    async def get_all_network_status(self) -> Dict[str, Dict[str, Any]]:
        """Get status information for all networks."""
        status_info = {}
        
        for network_name in self.networks.keys():
            try:
                status_info[network_name] = await self.get_network_status(network_name)
            except Exception as e:
                status_info[network_name] = {
                    "name": network_name,
                    "error": str(e)
                }
        
        return status_info
    
    async def monitor_networks(self) -> Dict[str, Any]:
        """Monitor all active networks for updates."""
        monitoring_data = {
            "timestamp": asyncio.get_event_loop().time(),
            "active_networks": len(self.active_networks),
            "networks": {}
        }
        
        for network_name in self.active_networks:
            try:
                network = self.networks[network_name]
                
                # Update block height and other monitoring data
                if network.is_connected:
                    # Get latest block info (implementation depends on network)
                    monitoring_data["networks"][network_name] = {
                        "status": "healthy",
                        "block_height": network.block_height,
                        "last_updated": asyncio.get_event_loop().time()
                    }
                else:
                    monitoring_data["networks"][network_name] = {
                        "status": "disconnected"
                    }
                    
            except Exception as e:
                monitoring_data["networks"][network_name] = {
                    "status": "error",
                    "error": str(e)
                }
        
        return monitoring_data
    
    def get_supported_networks(self) -> List[str]:
        """Get list of supported network types."""
        return [network_type.value for network_type in NetworkType]
    
    async def estimate_cross_chain_fees(self, transactions: Dict[str, Dict[str, Any]]) -> Dict[str, float]:
        """Estimate fees for cross-chain transactions."""
        fee_estimates = {}
        
        for network_name, tx_data in transactions.items():
            try:
                network = self.get_network(network_name)
                
                if not network.is_connected:
                    await self.connect_network(network_name)
                
                gas_estimate = await network.estimate_gas(tx_data)
                # Convert gas estimate to fee (implementation varies by network)
                fee_estimates[network_name] = gas_estimate * 0.00000001  # Placeholder calculation
                
            except Exception as e:
                fee_estimates[network_name] = None
                logger.error(f"Failed to estimate fees for {network_name}: {e}")
        
        return fee_estimates
