"""
Solana network implementation for Nivora AI SDK.
"""

import asyncio
import os
import json
from typing import Dict, Any, Optional, List
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.transaction import Transaction
from solders.system_program import transfer, TransferParams
from solana.rpc.async_api import AsyncClient
from solana.rpc.commitment import Confirmed, Finalized
from solana.rpc.types import TxOpts

from ..core.blockchain import BaseBlockchainNetwork, NetworkConfig
from ..utils.logger import get_logger
from ..utils.exceptions import NetworkException

logger = get_logger(__name__)


class SolanaNetwork(BaseBlockchainNetwork):
    """
    Solana blockchain network implementation.
    """
    
    def __init__(self, config: NetworkConfig):
        """Initialize Solana network."""
        super().__init__(config)
        self.client: Optional[AsyncClient] = None
        self.keypair: Optional[Keypair] = None
        
        # Default RPC URLs for Solana networks
        self.default_rpcs = {
            "mainnet": "https://api.mainnet-beta.solana.com",
            "testnet": "https://api.testnet.solana.com",
            "devnet": "https://api.devnet.solana.com",
        }
        
        # Map chain_id to network names for convenience
        self.chain_id_map = {
            101: "mainnet",
            102: "testnet", 
            103: "devnet",
        }
        
        logger.info(f"Initialized Solana network")
    
    async def connect(self) -> bool:
        """Connect to the Solana network."""
        try:
            # Determine RPC URL
            rpc_url = self.config.rpc_url
            if not rpc_url:
                if self.config.chain_id:
                    network_name = self.chain_id_map.get(self.config.chain_id, "devnet")
                    rpc_url = self.default_rpcs[network_name]
                else:
                    rpc_url = self.default_rpcs["devnet"]  # Default to devnet
            
            # Initialize Solana client
            self.client = AsyncClient(rpc_url)
            
            # Test connection by getting recent blockhash
            recent_blockhash = await self.client.get_latest_blockhash()
            if not recent_blockhash.value:
                raise NetworkException("Failed to get recent blockhash from Solana")
            
            # Get current slot (equivalent to block number)
            slot_response = await self.client.get_slot()
            self.block_height = slot_response.value
            
            # Setup keypair if private key is provided
            if self.config.private_key:
                # Convert private key to Solana keypair
                if isinstance(self.config.private_key, str):
                    # Assume it's a base58 encoded private key or secret key bytes
                    try:
                        import base58
                        secret_key = base58.b58decode(self.config.private_key)[:32]
                    except:
                        # Assume it's hex encoded
                        secret_key = bytes.fromhex(self.config.private_key.replace('0x', ''))
                    
                    self.keypair = Keypair.from_bytes(secret_key)
                else:
                    self.keypair = Keypair.from_bytes(self.config.private_key)
                
                logger.info(f"Setup Solana account: {self.keypair.pubkey()}")
            
            self.is_connected = True
            logger.info(f"Connected to Solana network (Slot: {self.block_height})")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to connect to Solana network: {e}")
            self.is_connected = False
            raise NetworkException(f"Solana connection failed: {e}")
    
    async def disconnect(self) -> None:
        """Disconnect from the Solana network."""
        if self.client:
            await self.client.close()
        self.client = None
        self.keypair = None
        self.is_connected = False
        logger.info("Disconnected from Solana network")
    
    async def deploy_contract(self, contract_code: str, constructor_args: List[Any] = None) -> str:
        """Deploy a program (smart contract) to Solana."""
        if not self.is_connected or not self.client:
            raise NetworkException("Not connected to Solana network")
        
        if not self.keypair:
            raise NetworkException("No keypair configured for deployment")
        
        try:
            # Solana program deployment is more complex than EVM chains
            # This is a simplified version - in production, use Anchor framework
            
            # For now, we'll create a simple data account to store agent info
            # This simulates a deployed "contract"
            
            # Generate a new account for the agent data
            agent_account = Keypair()
            
            # Calculate rent exemption for account
            min_balance_response = await self.client.get_minimum_balance_for_rent_exemption(1024)  # 1KB account
            min_balance = min_balance_response.value
            
            # Create account instruction
            from solders.system_program import create_account, CreateAccountParams
            
            create_account_ix = create_account(
                CreateAccountParams(
                    from_pubkey=self.keypair.pubkey(),
                    to_pubkey=agent_account.pubkey(),
                    lamports=min_balance,
                    space=1024,
                    owner=self.keypair.pubkey(),  # Owner is our keypair for simplicity
                )
            )
            
            # Create transaction
            recent_blockhash = await self.client.get_latest_blockhash()
            transaction = Transaction.new_unsigned([create_account_ix])
            transaction.partial_sign([self.keypair, agent_account], recent_blockhash.value.blockhash)
            
            # Send transaction
            result = await self.client.send_transaction(
                transaction, 
                opts=TxOpts(skip_confirmation=False, preflight_commitment=Confirmed)
            )
            
            # Wait for confirmation
            await self.client.confirm_transaction(result.value, commitment=Confirmed)
            
            agent_address = str(agent_account.pubkey())
            logger.info(f"Solana agent account created: {agent_address}")
            
            return agent_address
            
        except Exception as e:
            logger.error(f"Solana program deployment failed: {e}")
            raise NetworkException(f"Program deployment failed: {e}")
    
    async def call_contract(self, contract_address: str, method_name: str, args: List[Any] = None) -> Any:
        """Call a program method on Solana."""
        if not self.is_connected or not self.client:
            raise NetworkException("Not connected to Solana network")
        
        try:
            # Convert contract address to pubkey
            pubkey = Pubkey.from_string(contract_address)
            
            # Get account info (simulates calling a contract)
            account_info = await self.client.get_account_info(pubkey)
            
            if not account_info.value:
                raise NetworkException(f"Account {contract_address} not found")
            
            # For this simplified implementation, we'll just return account data
            # In a real Solana program, this would involve creating and sending instructions
            
            if method_name == "active":
                # Check if account exists and has data
                return account_info.value is not None
            elif method_name == "getBalance":
                return account_info.value.lamports if account_info.value else 0
            else:
                # Return account data for other methods
                return {
                    "method": method_name,
                    "args": args or [],
                    "account_data": account_info.value.data if account_info.value else None,
                    "owner": str(account_info.value.owner) if account_info.value else None
                }
                
        except Exception as e:
            logger.error(f"Solana program call failed: {e}")
            raise NetworkException(f"Program call failed: {e}")
    
    async def send_transaction(self, to_address: str, amount: float, data: str = None) -> str:
        """Send a transaction on Solana."""
        if not self.is_connected or not self.client:
            raise NetworkException("Not connected to Solana network")
        
        if not self.keypair:
            raise NetworkException("No keypair configured for transactions")
        
        try:
            # Convert amount to lamports (1 SOL = 1,000,000,000 lamports)
            amount_lamports = int(amount * 1_000_000_000)
            
            # Convert to address to pubkey
            to_pubkey = Pubkey.from_string(to_address)
            
            # Create transfer instruction
            transfer_ix = transfer(
                TransferParams(
                    from_pubkey=self.keypair.pubkey(),
                    to_pubkey=to_pubkey,
                    lamports=amount_lamports
                )
            )
            
            # Get recent blockhash
            recent_blockhash = await self.client.get_latest_blockhash()
            
            # Create and sign transaction
            transaction = Transaction.new_unsigned([transfer_ix])
            transaction.sign([self.keypair], recent_blockhash.value.blockhash)
            
            # Send transaction
            result = await self.client.send_transaction(
                transaction,
                opts=TxOpts(skip_confirmation=False, preflight_commitment=Confirmed)
            )
            
            tx_hash = str(result.value)
            logger.info(f"Solana transaction sent: {tx_hash}")
            
            return tx_hash
            
        except Exception as e:
            logger.error(f"Solana transaction failed: {e}")
            raise NetworkException(f"Transaction failed: {e}")
    
    async def get_balance(self, address: str) -> float:
        """Get account balance in SOL."""
        if not self.is_connected or not self.client:
            raise NetworkException("Not connected to Solana network")
        
        try:
            pubkey = Pubkey.from_string(address)
            balance_response = await self.client.get_balance(pubkey)
            balance_lamports = balance_response.value
            
            # Convert lamports to SOL
            balance_sol = balance_lamports / 1_000_000_000
            
            return float(balance_sol)
            
        except Exception as e:
            logger.error(f"Failed to get Solana balance: {e}")
            raise NetworkException(f"Balance query failed: {e}")
    
    async def get_transaction_status(self, tx_hash: str) -> Dict[str, Any]:
        """Get transaction status and details."""
        if not self.is_connected or not self.client:
            raise NetworkException("Not connected to Solana network")
        
        try:
            # Get transaction details
            transaction_response = await self.client.get_transaction(
                tx_hash, 
                commitment=Confirmed,
                max_supported_transaction_version=0
            )
            
            if not transaction_response.value:
                return {
                    "hash": tx_hash,
                    "status": "not_found",
                    "error": "Transaction not found"
                }
            
            transaction = transaction_response.value
            
            # Get current slot for confirmations
            current_slot = await self.client.get_slot()
            confirmations = current_slot.value - transaction.slot if transaction.slot else 0
            
            return {
                "hash": tx_hash,
                "status": "success" if transaction.meta and not transaction.meta.err else "failed",
                "slot": transaction.slot,
                "confirmations": confirmations,
                "fee": transaction.meta.fee if transaction.meta else 0,
                "compute_units_consumed": transaction.meta.compute_units_consumed if transaction.meta else 0,
                "block_time": transaction.block_time,
                "error": str(transaction.meta.err) if transaction.meta and transaction.meta.err else None
            }
            
        except Exception as e:
            logger.error(f"Failed to get Solana transaction status: {e}")
            raise NetworkException(f"Transaction status query failed: {e}")
    
    async def estimate_gas(self, transaction: Dict[str, Any]) -> int:
        """Estimate compute units for a transaction (Solana equivalent of gas)."""
        if not self.is_connected or not self.client:
            raise NetworkException("Not connected to Solana network")
        
        try:
            # Solana uses compute units instead of gas
            # For a simple transfer, it's typically around 150 compute units
            # For more complex operations, it can be up to 200,000 units per instruction
            
            instruction_type = transaction.get("instruction_type", "transfer")
            
            if instruction_type == "transfer":
                return 150
            elif instruction_type == "create_account":
                return 300
            elif instruction_type == "program_call":
                return 10000  # Estimate for program calls
            else:
                return 5000  # Default estimate
                
        except Exception as e:
            logger.error(f"Failed to estimate Solana compute units: {e}")
            return 5000  # Default fallback
    
    async def get_network_info(self) -> Dict[str, Any]:
        """Get detailed Solana network information."""
        if not self.is_connected or not self.client:
            raise NetworkException("Not connected to Solana network")
        
        try:
            # Get various network statistics
            slot = await self.client.get_slot()
            epoch_info = await self.client.get_epoch_info()
            version = await self.client.get_version()
            
            # Get cluster nodes
            cluster_nodes = await self.client.get_cluster_nodes()
            
            return {
                "network": "solana",
                "slot": slot.value,
                "epoch": epoch_info.value.epoch,
                "slot_index": epoch_info.value.slot_index,
                "slots_in_epoch": epoch_info.value.slots_in_epoch,
                "absolute_slot": epoch_info.value.absolute_slot,
                "version": version.value.solana_core,
                "feature_set": version.value.feature_set,
                "cluster_nodes": len(cluster_nodes.value) if cluster_nodes.value else 0,
                "is_connected": self.is_connected,
                "native_currency": "SOL",
                "block_time": 0.4,  # Solana average slot time in seconds
            }
            
        except Exception as e:
            logger.error(f"Failed to get Solana network info: {e}")
            raise NetworkException(f"Network info query failed: {e}")
    
    async def get_token_balance(self, token_mint: str, wallet_address: str) -> float:
        """Get SPL token balance."""
        if not self.is_connected or not self.client:
            raise NetworkException("Not connected to Solana network")
        
        try:
            from spl.token.constants import TOKEN_PROGRAM_ID
            
            wallet_pubkey = Pubkey.from_string(wallet_address)
            mint_pubkey = Pubkey.from_string(token_mint)
            
            # Get token accounts for the wallet
            token_accounts = await self.client.get_token_accounts_by_owner(
                wallet_pubkey,
                {"mint": mint_pubkey},
                commitment=Confirmed
            )
            
            if not token_accounts.value:
                return 0.0
            
            total_balance = 0.0
            
            for account_info in token_accounts.value:
                # Get account data
                account_data = await self.client.get_account_info(
                    account_info.pubkey,
                    commitment=Confirmed
                )
                
                if account_data.value:
                    # Parse token account data (simplified)
                    # In production, use proper SPL token parsing
                    balance_lamports = account_data.value.lamports
                    # Convert based on token decimals (assuming 9 decimals for simplicity)
                    balance = balance_lamports / 1_000_000_000
                    total_balance += balance
            
            return total_balance
            
        except Exception as e:
            logger.error(f"Failed to get Solana token balance: {e}")
            raise NetworkException(f"Token balance query failed: {e}")
    
    async def create_token_account(self, token_mint: str) -> str:
        """Create a new SPL token account."""
        if not self.is_connected or not self.client:
            raise NetworkException("Not connected to Solana network")
        
        if not self.keypair:
            raise NetworkException("No keypair configured")
        
        try:
            from spl.token.instructions import create_associated_token_account
            from spl.token.constants import TOKEN_PROGRAM_ID, ASSOCIATED_TOKEN_PROGRAM_ID
            
            mint_pubkey = Pubkey.from_string(token_mint)
            
            # Create associated token account instruction
            create_ata_ix = create_associated_token_account(
                payer=self.keypair.pubkey(),
                owner=self.keypair.pubkey(),
                mint=mint_pubkey,
                token_program_id=TOKEN_PROGRAM_ID,
                associated_token_program_id=ASSOCIATED_TOKEN_PROGRAM_ID
            )
            
            # Get recent blockhash
            recent_blockhash = await self.client.get_latest_blockhash()
            
            # Create and sign transaction
            transaction = Transaction.new_unsigned([create_ata_ix])
            transaction.sign([self.keypair], recent_blockhash.value.blockhash)
            
            # Send transaction
            result = await self.client.send_transaction(
                transaction,
                opts=TxOpts(skip_confirmation=False, preflight_commitment=Confirmed)
            )
            
            # Calculate the associated token account address
            from spl.token.constants import ASSOCIATED_TOKEN_PROGRAM_ID
            
            # This is a simplified calculation
            # In production, use proper associated token account derivation
            token_account_address = str(result.value)  # Simplified
            
            logger.info(f"Created Solana token account: {token_account_address}")
            return token_account_address
            
        except Exception as e:
            logger.error(f"Failed to create Solana token account: {e}")
            raise NetworkException(f"Token account creation failed: {e}")
    
    async def get_program_accounts(self, program_id: str, filters: List[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Get accounts owned by a program."""
        if not self.is_connected or not self.client:
            raise NetworkException("Not connected to Solana network")
        
        try:
            program_pubkey = Pubkey.from_string(program_id)
            
            # Get program accounts
            accounts_response = await self.client.get_program_accounts(
                program_pubkey,
                commitment=Confirmed
            )
            
            accounts = []
            for account_info in accounts_response.value:
                accounts.append({
                    "pubkey": str(account_info.pubkey),
                    "account": {
                        "lamports": account_info.account.lamports,
                        "data": account_info.account.data,
                        "owner": str(account_info.account.owner),
                        "executable": account_info.account.executable,
                        "rent_epoch": account_info.account.rent_epoch
                    }
                })
            
            return accounts
            
        except Exception as e:
            logger.error(f"Failed to get Solana program accounts: {e}")
            raise NetworkException(f"Program accounts query failed: {e}")
