"""
Custom exceptions for Nivora AI SDK.
"""

from typing import Optional, Dict, Any


class NivoraAIException(Exception):
    """Base exception for Nivora AI SDK."""
    
    def __init__(self, message: str, code: Optional[str] = None, details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.message = message
        self.code = code
        self.details = details or {}


class ConfigurationError(NivoraAIException):
    """Configuration related errors."""
    pass


class NetworkError(NivoraAIException):
    """Network related errors."""
    pass


class BlockchainError(NivoraAIException):
    """Blockchain operation errors."""
    pass


class DeploymentError(NivoraAIException):
    """Deployment related errors."""
    pass


class AgentError(NivoraAIException):
    """Agent related errors."""
    pass


class MonetizationError(NivoraAIException):
    """Monetization related errors."""
    pass


class WebSocketException(NivoraAIException):
    """WebSocket related errors."""
    pass


class DatabaseError(NivoraAIException):
    """Database related errors."""
    pass


class AuthenticationError(NivoraAIException):
    """Authentication related errors."""
    pass


class ValidationError(NivoraAIException):
    """Validation related errors."""
    pass