"""
Binance Smart Chain (BSC) network implementation for Nivora AI SDK.
"""

import os
from typing import Dict, Any, Optional, List
from web3 import Web3

from .ethereum import EthereumNetwork
from ..core.blockchain import NetworkConfig
from ..utils.logger import get_logger
from ..utils.exceptions import NetworkException

logger = get_logger(__name__)


class BSCNetwork(EthereumNetwork):
    """
    Binance Smart Chain blockchain network implementation.
    Inherits from EthereumNetwork since BSC is EVM-compatible.
    """
    
    def __init__(self, config: NetworkConfig):
        """Initialize BSC network."""
        super().__init__(config)
        
        # BSC-specific configurations
        self.gas_price_multiplier = 1.1
        self.max_gas_price = Web3.to_wei(20, 'gwei')  # BSC typically has low gas prices
        
        # Default RPC URLs for BSC networks
        self.default_rpcs = {
            56: "https://bsc-dataseed.binance.org/",  # BSC Mainnet
            97: "https://data-seed-prebsc-1-s1.binance.org:8545/",  # BSC Testnet
        }
        
        logger.info(f"Initialized BSC network with chain_id {config.chain_id}")
    
    async def connect(self) -> bool:
        """Connect to the BSC network."""
        try:
            # Setup RPC URL for BSC
            rpc_url = self.config.rpc_url
            if not rpc_url and self.config.chain_id:
                rpc_url = self.default_rpcs.get(self.config.chain_id)
                
                # Additional BSC RPC endpoints for redundancy
                if self.config.chain_id == 56 and not rpc_url:
                    rpc_urls = [
                        "https://bsc-dataseed1.binance.org/",
                        "https://bsc-dataseed2.binance.org/",
                        "https://bsc-dataseed3.binance.org/",
                        "https://bsc-dataseed4.binance.org/",
                    ]
                    rpc_url = rpc_urls[0]  # Use first available
                elif self.config.chain_id == 97 and not rpc_url:
                    rpc_url = "https://data-seed-prebsc-2-s1.binance.org:8545/"
            
            if not rpc_url:
                raise NetworkException("No RPC URL configured for BSC")
            
            # Update config with BSC RPC
            self.config.rpc_url = rpc_url
            
            # Initialize Web3 connection
            self.web3 = Web3(Web3.HTTPProvider(rpc_url))
            
            # Test connection
            if not self.web3.is_connected():
                raise NetworkException("Failed to connect to BSC RPC")
            
            # Get latest block to verify connection
            latest_block = self.web3.eth.get_block('latest')
            self.block_height = latest_block['number']
            
            # Setup account if private key is provided
            if self.config.private_key:
                self.account = self.web3.eth.account.from_key(self.config.private_key)
                logger.info(f"Setup BSC account: {self.account.address}")
            
            self.is_connected = True
            logger.info(f"Connected to BSC network (Chain ID: {self.web3.eth.chain_id}, Block: {self.block_height})")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to connect to BSC network: {e}")
            self.is_connected = False
            raise NetworkException(f"BSC connection failed: {e}")
    
    async def _get_gas_price(self) -> int:
        """Get current gas price optimized for BSC."""
        try:
            # Get base gas price
            base_gas_price = self.web3.eth.gas_price
            
            # BSC typically has very low gas prices (3-5 Gwei)
            # Apply conservative multiplier
            adjusted_gas_price = int(base_gas_price * self.gas_price_multiplier)
            
            # Ensure minimum gas price for BSC (3 Gwei)
            min_gas_price = Web3.to_wei(3, 'gwei')
            adjusted_gas_price = max(adjusted_gas_price, min_gas_price)
            
            # Cap at maximum gas price
            final_gas_price = min(adjusted_gas_price, self.max_gas_price)
            
            logger.debug(f"BSC gas price: {Web3.from_wei(final_gas_price, 'gwei')} Gwei")
            return final_gas_price
            
        except Exception as e:
            logger.warning(f"Failed to get BSC gas price, using default: {e}")
            return Web3.to_wei(5, 'gwei')  # Default 5 Gwei for BSC
    
    async def get_balance(self, address: str) -> float:
        """Get account balance in BNB."""
        if not self.is_connected or not self.web3:
            raise NetworkException("Not connected to BSC network")
        
        try:
            balance_wei = self.web3.eth.get_balance(address)
            balance_bnb = Web3.from_wei(balance_wei, 'ether')  # BNB has same decimals as ETH
            return float(balance_bnb)
            
        except Exception as e:
            logger.error(f"Failed to get BSC balance: {e}")
            raise NetworkException(f"Balance query failed: {e}")
    
    async def get_transaction_status(self, tx_hash: str) -> Dict[str, Any]:
        """Get transaction status optimized for BSC."""
        status = await super().get_transaction_status(tx_hash)
        
        # Update currency references for BSC
        status["network"] = "bsc"
        status["native_currency"] = "BNB"
        
        return status
    
    async def get_network_info(self) -> Dict[str, Any]:
        """Get detailed BSC network information."""
        info = await super().get_network_info()
        
        # Update network-specific information
        info.update({
            "network": "bsc",
            "native_currency": "BNB",
            "block_time": 3.0,  # BSC average block time in seconds
            "finality_blocks": 15,  # Blocks for finality
            "validator_count": 21,  # BSC has 21 validators
        })
        
        return info
    
    async def get_bep20_token_balance(self, token_address: str, wallet_address: str) -> float:
        """Get BEP-20 token balance on BSC."""
        # BEP-20 is compatible with ERC-20 standard
        return await self.get_token_balance(token_address, wallet_address)
    
    async def get_token_balance(self, token_address: str, wallet_address: str) -> float:
        """Get BEP-20 token balance on BSC."""
        if not self.is_connected or not self.web3:
            raise NetworkException("Not connected to BSC network")
        
        try:
            # BEP-20 ABI (same as ERC-20)
            bep20_abi = [
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
                },
                {
                    "constant": True,
                    "inputs": [],
                    "name": "symbol",
                    "outputs": [{"name": "", "type": "string"}],
                    "type": "function"
                }
            ]
            
            # Create contract instance
            contract = self.web3.eth.contract(address=token_address, abi=bep20_abi)
            
            # Get balance and decimals
            balance = contract.functions.balanceOf(wallet_address).call()
            decimals = contract.functions.decimals().call()
            
            # Convert to human readable format
            balance_formatted = balance / (10 ** decimals)
            
            return float(balance_formatted)
            
        except Exception as e:
            logger.error(f"Failed to get BSC token balance: {e}")
            raise NetworkException(f"Token balance query failed: {e}")
    
    async def get_pancakeswap_price(self, token_address: str, base_token: str = "0xe9e7CEA3DedcA5984780Bafc599bD69ADd087D56") -> float:
        """Get token price from PancakeSwap (BUSD is default base token)."""
        if not self.is_connected or not self.web3:
            raise NetworkException("Not connected to BSC network")
        
        try:
            # PancakeSwap V2 Router address
            pancake_router = "0x10ED43C718714eb63d5aA57B78B54704E256024E"
            
            # Router ABI for getAmountsOut
            router_abi = [
                {
                    "inputs": [
                        {"internalType": "uint256", "name": "amountIn", "type": "uint256"},
                        {"internalType": "address[]", "name": "path", "type": "address[]"}
                    ],
                    "name": "getAmountsOut",
                    "outputs": [{"internalType": "uint256[]", "name": "amounts", "type": "uint256[]"}],
                    "stateMutability": "view",
                    "type": "function"
                }
            ]
            
            # Create router contract instance
            router_contract = self.web3.eth.contract(address=pancake_router, abi=router_abi)
            
            # Get price for 1 token
            amount_in = 10 ** 18  # 1 token with 18 decimals
            path = [token_address, base_token]
            
            amounts_out = router_contract.functions.getAmountsOut(amount_in, path).call()
            
            # Convert to price (assuming base token has 18 decimals)
            price = amounts_out[1] / (10 ** 18)
            
            return float(price)
            
        except Exception as e:
            logger.error(f"Failed to get PancakeSwap price: {e}")
            return 0.0
    
    async def estimate_gas(self, transaction: Dict[str, Any]) -> int:
        """Estimate gas for a transaction on BSC."""
        if not self.is_connected or not self.web3:
            raise NetworkException("Not connected to BSC network")
        
        try:
            gas_estimate = self.web3.eth.estimate_gas(transaction)
            
            # Add BSC-specific buffer (smaller than Ethereum due to lower costs)
            buffered_gas = int(gas_estimate * 1.05)
            
            return buffered_gas
            
        except Exception as e:
            logger.error(f"Failed to estimate BSC gas: {e}")
            raise NetworkException(f"Gas estimation failed: {e}")
    
    async def get_validator_info(self) -> Dict[str, Any]:
        """Get BSC validator information."""
        if not self.is_connected or not self.web3:
            raise NetworkException("Not connected to BSC network")
        
        try:
            # BSC Validator Set contract address
            validator_set_address = "0x0000000000000000000000000000000000001000"
            
            # Get current validators (simplified)
            latest_block = self.web3.eth.get_block('latest')
            
            return {
                "current_validators": 21,  # BSC has 21 active validators
                "latest_block": latest_block['number'],
                "block_producer": latest_block.get('miner', 'Unknown'),
                "block_time": 3.0,
                "consensus": "Proof of Staked Authority (PoSA)"
            }
            
        except Exception as e:
            logger.error(f"Failed to get BSC validator info: {e}")
            return {"error": str(e)}
