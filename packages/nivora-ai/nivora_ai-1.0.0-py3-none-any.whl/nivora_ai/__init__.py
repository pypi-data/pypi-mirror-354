"""
Nivora AI SDK - Comprehensive Python-based SDK and framework for deploying, 
scaling, and monetizing AI agents across multiple blockchain networks.
"""

__version__ = "0.1.0"
__author__ = "Nivora AI Team"
__email__ = "support@nivora-ai.com"
__description__ = "Deploy, scale, and monetize AI agents across multiple blockchains with zero configuration"

from .core.agent import AIAgent, AgentConfig
from .core.deployment import DeploymentManager
from .core.blockchain import BlockchainManager
from .core.monetization import MonetizationManager
from .core.interoperability import CrossChainManager
from .utils.config import Config
from .utils.exceptions import NivoraAIException

__all__ = [
    "AIAgent",
    "AgentConfig", 
    "DeploymentManager",
    "BlockchainManager",
    "MonetizationManager",
    "CrossChainManager",
    "Config",
    "NivoraAIException",
]
