"""
Configuration management for Nivora AI SDK.
"""

import os
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from pathlib import Path

from .logger import get_logger

logger = get_logger(__name__)


@dataclass
class DatabaseConfig:
    """Database configuration."""
    url: str = ""
    host: str = "localhost"
    port: int = 5432
    name: str = "nivora_ai"
    user: str = "nivora"
    password: str = ""
    pool_size: int = 10
    max_overflow: int = 20
    echo: bool = False


@dataclass
class RedisConfig:
    """Redis configuration."""
    url: str = ""
    host: str = "localhost"
    port: int = 6379
    db: int = 0
    password: Optional[str] = None
    max_connections: int = 10


@dataclass
class NetworkConfig:
    """Network configuration for blockchain."""
    name: str
    type: str
    rpc_url: str
    chain_id: Optional[int] = None
    private_key: Optional[str] = None
    gas_price: Optional[int] = None
    gas_limit: Optional[int] = None
    enabled: bool = True


@dataclass
class APIConfig:
    """API configuration."""
    host: str = "0.0.0.0"
    port: int = 8000
    workers: int = 1
    reload: bool = False
    debug: bool = False
    cors_origins: List[str] = field(default_factory=lambda: ["*"])
    api_keys: List[str] = field(default_factory=lambda: ["demo-key"])
    rate_limit: int = 100  # requests per minute
    request_timeout: int = 30  # seconds


@dataclass
class CeleryConfig:
    """Celery configuration."""
    broker_url: str = "redis://localhost:6379/0"
    result_backend: str = "redis://localhost:6379/0"
    task_serializer: str = "json"
    result_serializer: str = "json"
    accept_content: List[str] = field(default_factory=lambda: ["json"])
    timezone: str = "UTC"
    enable_utc: bool = True
    task_routes: Dict[str, Any] = field(default_factory=dict)


@dataclass
class LoggingConfig:
    """Logging configuration."""
    level: str = "INFO"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    file_path: Optional[str] = None
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    backup_count: int = 5
    json_format: bool = False


@dataclass
class SecurityConfig:
    """Security configuration."""
    secret_key: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expiration: int = 3600  # seconds
    bcrypt_rounds: int = 12
    rate_limit_enabled: bool = True
    cors_enabled: bool = True
    https_only: bool = False


@dataclass
class MonitoringConfig:
    """Monitoring configuration."""
    enabled: bool = True
    metrics_enabled: bool = True
    health_check_interval: int = 60  # seconds
    alert_enabled: bool = True
    prometheus_enabled: bool = False
    prometheus_port: int = 9090


class Config:
    """
    Main configuration class for Nivora AI SDK.
    """
    
    def __init__(self, config_file: Optional[str] = None):
        """Initialize configuration."""
        self.config_file = config_file
        self.environment = os.getenv("ENVIRONMENT", "development")
        
        # Initialize configuration sections
        self.database = DatabaseConfig()
        self.redis = RedisConfig()
        self.api = APIConfig()
        self.celery = CeleryConfig()
        self.logging = LoggingConfig()
        self.security = SecurityConfig()
        self.monitoring = MonitoringConfig()
        
        # Network configurations
        self.networks: Dict[str, NetworkConfig] = {}
        
        # Load configuration
        self._load_from_environment()
        
        if config_file:
            self._load_from_file(config_file)
        
        # Validate configuration
        self._validate()
        
        logger.info(f"Configuration loaded for environment: {self.environment}")
    
    def _load_from_environment(self) -> None:
        """Load configuration from environment variables."""
        # Database configuration
        self.database.url = os.getenv("DATABASE_URL", "")
        self.database.host = os.getenv("PGHOST", self.database.host)
        self.database.port = int(os.getenv("PGPORT", str(self.database.port)))
        self.database.name = os.getenv("PGDATABASE", self.database.name)
        self.database.user = os.getenv("PGUSER", self.database.user)
        self.database.password = os.getenv("PGPASSWORD", self.database.password)
        
        # If DATABASE_URL is not provided, construct it
        if not self.database.url:
            self.database.url = (
                f"postgresql://{self.database.user}:{self.database.password}@"
                f"{self.database.host}:{self.database.port}/{self.database.name}"
            )
        
        # Redis configuration
        self.redis.url = os.getenv("REDIS_URL", "")
        self.redis.host = os.getenv("REDIS_HOST", self.redis.host)
        self.redis.port = int(os.getenv("REDIS_PORT", str(self.redis.port)))
        self.redis.db = int(os.getenv("REDIS_DB", str(self.redis.db)))
        self.redis.password = os.getenv("REDIS_PASSWORD")
        
        if not self.redis.url:
            auth_part = f":{self.redis.password}@" if self.redis.password else ""
            self.redis.url = f"redis://{auth_part}{self.redis.host}:{self.redis.port}/{self.redis.db}"
        
        # API configuration
        self.api.host = os.getenv("HOST", self.api.host)
        self.api.port = int(os.getenv("PORT", str(self.api.port)))
        self.api.workers = int(os.getenv("WORKERS", str(self.api.workers)))
        self.api.debug = os.getenv("DEBUG", "false").lower() == "true"
        self.api.reload = os.getenv("RELOAD", "false").lower() == "true"
        
        # API keys
        api_keys_env = os.getenv("NIVORA_API_KEYS", "demo-key")
        self.api.api_keys = api_keys_env.split(",")
        
        # CORS origins
        cors_origins_env = os.getenv("CORS_ORIGINS", "*")
        self.api.cors_origins = cors_origins_env.split(",")
        
        # Celery configuration
        self.celery.broker_url = os.getenv("CELERY_BROKER_URL", self.redis.url)
        self.celery.result_backend = os.getenv("CELERY_RESULT_BACKEND", self.redis.url)
        
        # Logging configuration
        self.logging.level = os.getenv("LOG_LEVEL", self.logging.level)
        self.logging.file_path = os.getenv("LOG_FILE")
        self.logging.json_format = os.getenv("LOG_JSON", "false").lower() == "true"
        
        # Security configuration
        self.security.secret_key = os.getenv("SECRET_KEY", self.security.secret_key)
        self.security.https_only = os.getenv("HTTPS_ONLY", "false").lower() == "true"
        
        # Monitoring configuration
        self.monitoring.enabled = os.getenv("MONITORING_ENABLED", "true").lower() == "true"
        self.monitoring.prometheus_enabled = os.getenv("PROMETHEUS_ENABLED", "false").lower() == "true"
        self.monitoring.prometheus_port = int(os.getenv("PROMETHEUS_PORT", str(self.monitoring.prometheus_port)))
        
        # Load network configurations
        self._load_network_configs()
    
    def _load_network_configs(self) -> None:
        """Load blockchain network configurations from environment."""
        # Ethereum configuration
        if os.getenv("ETHEREUM_RPC_URL"):
            self.networks["ethereum"] = NetworkConfig(
                name="ethereum",
                type="ethereum",
                rpc_url=os.getenv("ETHEREUM_RPC_URL", ""),
                chain_id=int(os.getenv("ETHEREUM_CHAIN_ID", "1")),
                private_key=os.getenv("ETHEREUM_PRIVATE_KEY"),
                gas_price=int(os.getenv("ETHEREUM_GAS_PRICE", "0")) if os.getenv("ETHEREUM_GAS_PRICE") else None,
                gas_limit=int(os.getenv("ETHEREUM_GAS_LIMIT", "0")) if os.getenv("ETHEREUM_GAS_LIMIT") else None
            )
        
        # Polygon configuration
        if os.getenv("POLYGON_RPC_URL"):
            self.networks["polygon"] = NetworkConfig(
                name="polygon",
                type="polygon",
                rpc_url=os.getenv("POLYGON_RPC_URL", ""),
                chain_id=int(os.getenv("POLYGON_CHAIN_ID", "137")),
                private_key=os.getenv("POLYGON_PRIVATE_KEY"),
                gas_price=int(os.getenv("POLYGON_GAS_PRICE", "0")) if os.getenv("POLYGON_GAS_PRICE") else None,
                gas_limit=int(os.getenv("POLYGON_GAS_LIMIT", "0")) if os.getenv("POLYGON_GAS_LIMIT") else None
            )
        
        # BSC configuration
        if os.getenv("BSC_RPC_URL"):
            self.networks["bsc"] = NetworkConfig(
                name="bsc",
                type="bsc",
                rpc_url=os.getenv("BSC_RPC_URL", ""),
                chain_id=int(os.getenv("BSC_CHAIN_ID", "56")),
                private_key=os.getenv("BSC_PRIVATE_KEY"),
                gas_price=int(os.getenv("BSC_GAS_PRICE", "0")) if os.getenv("BSC_GAS_PRICE") else None,
                gas_limit=int(os.getenv("BSC_GAS_LIMIT", "0")) if os.getenv("BSC_GAS_LIMIT") else None
            )
        
        # Solana configuration
        if os.getenv("SOLANA_RPC_URL"):
            self.networks["solana"] = NetworkConfig(
                name="solana",
                type="solana",
                rpc_url=os.getenv("SOLANA_RPC_URL", ""),
                chain_id=int(os.getenv("SOLANA_CLUSTER_ID", "101")),
                private_key=os.getenv("SOLANA_PRIVATE_KEY")
            )
    
    def _load_from_file(self, config_file: str) -> None:
        """Load configuration from file."""
        try:
            import yaml
            
            config_path = Path(config_file)
            if not config_path.exists():
                logger.warning(f"Configuration file not found: {config_file}")
                return
            
            with open(config_path, 'r') as f:
                if config_file.endswith('.yaml') or config_file.endswith('.yml'):
                    config_data = yaml.safe_load(f)
                elif config_file.endswith('.json'):
                    import json
                    config_data = json.load(f)
                else:
                    logger.warning(f"Unsupported configuration file format: {config_file}")
                    return
            
            # Update configuration with file data
            self._update_from_dict(config_data)
            
            logger.info(f"Configuration loaded from file: {config_file}")
            
        except ImportError:
            logger.warning("PyYAML not installed, skipping YAML configuration file")
        except Exception as e:
            logger.error(f"Failed to load configuration from file: {e}")
    
    def _update_from_dict(self, config_data: Dict[str, Any]) -> None:
        """Update configuration from dictionary."""
        # Update database config
        if "database" in config_data:
            db_config = config_data["database"]
            for key, value in db_config.items():
                if hasattr(self.database, key):
                    setattr(self.database, key, value)
        
        # Update Redis config
        if "redis" in config_data:
            redis_config = config_data["redis"]
            for key, value in redis_config.items():
                if hasattr(self.redis, key):
                    setattr(self.redis, key, value)
        
        # Update API config
        if "api" in config_data:
            api_config = config_data["api"]
            for key, value in api_config.items():
                if hasattr(self.api, key):
                    setattr(self.api, key, value)
        
        # Update network configs
        if "networks" in config_data:
            for network_name, network_config in config_data["networks"].items():
                self.networks[network_name] = NetworkConfig(
                    name=network_name,
                    **network_config
                )
    
    def _validate(self) -> None:
        """Validate configuration."""
        # Validate required fields
        if not self.database.url:
            raise ValueError("Database URL is required")
        
        if not self.redis.url:
            raise ValueError("Redis URL is required")
        
        if self.environment == "production":
            if self.security.secret_key == "change-me-in-production":
                raise ValueError("Secret key must be changed in production")
            
            if "demo-key" in self.api.api_keys:
                logger.warning("Demo API key detected in production environment")
        
        # Validate network configurations
        for network_name, network_config in self.networks.items():
            if not network_config.rpc_url:
                logger.warning(f"RPC URL not configured for network: {network_name}")
    
    def get_database_url(self, async_driver: bool = True) -> str:
        """Get database URL with appropriate driver."""
        if async_driver and self.database.url.startswith("postgresql://"):
            return self.database.url.replace("postgresql://", "postgresql+asyncpg://")
        return self.database.url
    
    def get_network_config(self, network_name: str) -> Optional[NetworkConfig]:
        """Get network configuration by name."""
        return self.networks.get(network_name)
    
    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self.environment == "development"
    
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.environment == "production"
    
    def is_testing(self) -> bool:
        """Check if running in testing environment."""
        return self.environment == "testing"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return {
            "environment": self.environment,
            "database": {
                "host": self.database.host,
                "port": self.database.port,
                "name": self.database.name,
                "user": self.database.user,
                # Don't include password in dict
            },
            "redis": {
                "host": self.redis.host,
                "port": self.redis.port,
                "db": self.redis.db,
            },
            "api": {
                "host": self.api.host,
                "port": self.api.port,
                "workers": self.api.workers,
                "debug": self.api.debug,
            },
            "networks": {
                name: {
                    "name": config.name,
                    "type": config.type,
                    "chain_id": config.chain_id,
                    "enabled": config.enabled,
                    # Don't include sensitive data
                } for name, config in self.networks.items()
            },
            "monitoring": {
                "enabled": self.monitoring.enabled,
                "metrics_enabled": self.monitoring.metrics_enabled,
                "prometheus_enabled": self.monitoring.prometheus_enabled,
            }
        }
    
    def __str__(self) -> str:
        """String representation of configuration."""
        return f"Config(environment={self.environment}, networks={list(self.networks.keys())})"
    
    def __repr__(self) -> str:
        """Detailed representation of configuration."""
        return (
            f"Config("
            f"environment={self.environment}, "
            f"database_host={self.database.host}, "
            f"api_port={self.api.port}, "
            f"networks={list(self.networks.keys())}"
            f")"
        )


# Global configuration instance
_config: Optional[Config] = None


def get_config() -> Config:
    """Get global configuration instance."""
    global _config
    if _config is None:
        _config = Config()
    return _config


def set_config(config: Config) -> None:
    """Set global configuration instance."""
    global _config
    _config = config
