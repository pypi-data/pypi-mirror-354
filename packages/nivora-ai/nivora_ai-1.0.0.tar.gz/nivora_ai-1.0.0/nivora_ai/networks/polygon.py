"""
Polygon (Matic) network implementation for Nivora AI SDK.
"""

import os
from typing import Dict, Any, Optional, List
from web3 import Web3

from .ethereum import EthereumNetwork
from ..core.blockchain import NetworkConfig
from ..utils.logger import get_logger
from ..utils.exceptions import NetworkException

logger = get_logger(__name__)


class PolygonNetwork(EthereumNetwork):
    """
    Polygon blockchain network implementation.
    Inherits from EthereumNetwork since Polygon is EVM-compatible.
    """
    
    def __init__(self, config: NetworkConfig):
        """Initialize Polygon network."""
        super().__init__(config)
        
        # Polygon-specific configurations
        self.gas_price_multiplier = 1.2  # Slightly higher for faster confirmations
        self.max_gas_price = Web3.to_wei(500, 'gwei')  # Higher limit for Polygon
        
        # Default RPC URLs for Polygon networks
        self.default_rpcs = {
            137: "https://polygon-mainnet.infura.io/v3/",  # Polygon Mainnet
            80001: "https://polygon-mumbai.infura.io/v3/",  # Mumbai testnet
        }
        
        logger.info(f"Initialized Polygon network with chain_id {config.chain_id}")
    
    async def connect(self) -> bool:
        """Connect to the Polygon network."""
        try:
            # Get Infura API key from environment
            infura_key = os.getenv("INFURA_API_KEY", "demo")
            
            # Setup RPC URL for Polygon
            rpc_url = self.config.rpc_url
            if not rpc_url and self.config.chain_id:
                base_url = self.default_rpcs.get(self.config.chain_id)
                if base_url:
                    rpc_url = f"{base_url}{infura_key}"
                elif self.config.chain_id == 137:
                    # Fallback to public RPC
                    rpc_url = "https://polygon-rpc.com"
                elif self.config.chain_id == 80001:
                    # Fallback to Mumbai public RPC
                    rpc_url = "https://rpc-mumbai.maticvigil.com"
            
            if not rpc_url:
                raise NetworkException("No RPC URL configured for Polygon")
            
            # Update config with Polygon RPC
            self.config.rpc_url = rpc_url
            
            # Use parent Ethereum connect method (EVM compatible)
            result = await super().connect()
            
            if result:
                logger.info(f"Connected to Polygon network (Chain ID: {self.web3.eth.chain_id}, Block: {self.block_height})")
            
            return result
            
        except Exception as e:
            logger.error(f"Failed to connect to Polygon network: {e}")
            self.is_connected = False
            raise NetworkException(f"Polygon connection failed: {e}")
    
    async def _get_gas_price(self) -> int:
        """Get current gas price optimized for Polygon."""
        try:
            # Get base gas price
            base_gas_price = self.web3.eth.gas_price
            
            # Polygon typically has very low gas prices
            # Apply different multiplier strategy
            if base_gas_price < Web3.to_wei(1, 'gwei'):
                # Very low gas price, use higher multiplier
                adjusted_gas_price = int(base_gas_price * 2.0)
            else:
                # Normal multiplier
                adjusted_gas_price = int(base_gas_price * self.gas_price_multiplier)
            
            # Ensure minimum gas price for Polygon
            min_gas_price = Web3.to_wei(1, 'gwei')
            adjusted_gas_price = max(adjusted_gas_price, min_gas_price)
            
            # Cap at maximum gas price
            final_gas_price = min(adjusted_gas_price, self.max_gas_price)
            
            logger.debug(f"Polygon gas price: {Web3.from_wei(final_gas_price, 'gwei')} Gwei")
            return final_gas_price
            
        except Exception as e:
            logger.warning(f"Failed to get Polygon gas price, using default: {e}")
            return Web3.to_wei(2, 'gwei')  # Default 2 Gwei for Polygon
    
    async def get_balance(self, address: str) -> float:
        """Get account balance in MATIC."""
        if not self.is_connected or not self.web3:
            raise NetworkException("Not connected to Polygon network")
        
        try:
            balance_wei = self.web3.eth.get_balance(address)
            balance_matic = Web3.from_wei(balance_wei, 'ether')  # MATIC has same decimals as ETH
            return float(balance_matic)
            
        except Exception as e:
            logger.error(f"Failed to get Polygon balance: {e}")
            raise NetworkException(f"Balance query failed: {e}")
    
    async def get_transaction_status(self, tx_hash: str) -> Dict[str, Any]:
        """Get transaction status optimized for Polygon."""
        status = await super().get_transaction_status(tx_hash)
        
        # Update currency references for Polygon
        status["network"] = "polygon"
        status["native_currency"] = "MATIC"
        
        return status
    
    async def send_transaction(self, to_address: str, amount: float, data: str = None) -> str:
        """Send a transaction on Polygon."""
        if not self.is_connected or not self.web3:
            raise NetworkException("Not connected to Polygon network")
        
        if not self.account:
            raise NetworkException("No account configured for transactions")
        
        try:
            # Convert amount to Wei (MATIC uses same decimals as ETH)
            amount_wei = Web3.to_wei(amount, 'ether')
            
            # Get gas price optimized for Polygon
            gas_price = await self._get_gas_price()
            
            # Build transaction with Polygon-optimized settings
            transaction = {
                'to': to_address,
                'value': amount_wei,
                'gas': 21000,  # Standard gas for MATIC transfer
                'gasPrice': gas_price,
                'nonce': self.web3.eth.get_transaction_count(self.account.address),
            }
            
            if data:
                transaction['data'] = data
                # Estimate gas for data transaction
                estimated_gas = self.web3.eth.estimate_gas(transaction)
                # Add buffer for Polygon
                transaction['gas'] = int(estimated_gas * 1.1)
            
            # Sign and send transaction
            signed_txn = self.web3.eth.account.sign_transaction(transaction, self.config.private_key)
            tx_hash = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
            
            logger.info(f"Polygon transaction sent: {tx_hash.hex()}")
            return tx_hash.hex()
            
        except Exception as e:
            logger.error(f"Polygon transaction failed: {e}")
            raise NetworkException(f"Transaction failed: {e}")
    
    async def get_network_info(self) -> Dict[str, Any]:
        """Get detailed Polygon network information."""
        info = await super().get_network_info()
        
        # Update network-specific information
        info.update({
            "network": "polygon",
            "native_currency": "MATIC",
            "block_time": 2.1,  # Polygon average block time in seconds
            "finality_blocks": 128,  # Blocks for finality
        })
        
        return info
    
    async def get_token_balance(self, token_address: str, wallet_address: str) -> float:
        """Get ERC-20 token balance on Polygon."""
        if not self.is_connected or not self.web3:
            raise NetworkException("Not connected to Polygon network")
        
        try:
            # ERC-20 ABI for balanceOf function
            erc20_abi = [
                {
                    "constant": True,
                    "inputs": [{"name": "_owner", "type": "address"}],
                    "name": "balanceOf",
                    "outputs": [{"name": "balance", "type": "uint256"}],
                    "type": "function"
                },
                {
                    "constant": True,
                    "inputs": [],
                    "name": "decimals",
                    "outputs": [{"name": "", "type": "uint8"}],
                    "type": "function"
                }
            ]
            
            # Create contract instance
            contract = self.web3.eth.contract(address=token_address, abi=erc20_abi)
            
            # Get balance and decimals
            balance = contract.functions.balanceOf(wallet_address).call()
            decimals = contract.functions.decimals().call()
            
            # Convert to human readable format
            balance_formatted = balance / (10 ** decimals)
            
            return float(balance_formatted)
            
        except Exception as e:
            logger.error(f"Failed to get Polygon token balance: {e}")
            raise NetworkException(f"Token balance query failed: {e}")
    
    async def estimate_gas(self, transaction: Dict[str, Any]) -> int:
        """Estimate gas for a transaction on Polygon."""
        if not self.is_connected or not self.web3:
            raise NetworkException("Not connected to Polygon network")
        
        try:
            gas_estimate = self.web3.eth.estimate_gas(transaction)
            
            # Add Polygon-specific buffer
            buffered_gas = int(gas_estimate * 1.1)
            
            return buffered_gas
            
        except Exception as e:
            logger.error(f"Failed to estimate Polygon gas: {e}")
            raise NetworkException(f"Gas estimation failed: {e}")
