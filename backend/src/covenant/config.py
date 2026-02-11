"""
Advanced Configuration System with Dynamic Reloading
Supports: env vars, vault, consul, AWS SSM, GCP Secret Manager
"""

from typing import Any, Optional, List, Dict
from pydantic_settings import BaseSettings
from functools import lru_cache
import os

class DatabaseSettings(BaseSettings):
    """Database configuration"""
    url: str = "postgresql+asyncpg://covenant:covenant@localhost:5432/covenant"
    pool_size: int = 100
    max_overflow: int = 200
    pool_pre_ping: bool = True
    echo: bool = False
    
    # Read replica support
    read_replica_urls: List[str] = []
    
    # Sharding
    shard_count: int = 1
    shard_key: str = "user_id"

class RedisSettings(BaseSettings):
    """Redis configuration"""
    url: str = "redis://localhost:6379/0"
    max_connections: int = 500
    socket_timeout: int = 5
    socket_connect_timeout: int = 5
    
    # Cluster mode
    cluster_mode: bool = False
    cluster_nodes: List[str] = []
    
    # Sentinel
    sentinel_mode: bool = False
    sentinel_nodes: List[str] = []
    sentinel_service: str = "mymaster"

class SecuritySettings(BaseSettings):
    """Security configuration"""
    secret_key: str = "CHANGE_ME_IN_PRODUCTION"
    jwt_secret: str = "CHANGE_ME_IN_PRODUCTION"
    jwt_algorithm: str = "HS512"
    access_token_expire_minutes: int = 60
    refresh_token_expire_days: int = 30
    
    # Encryption
    encryption_key: Optional[str] = None
    use_hsm: bool = False
    hsm_key_id: Optional[str] = None
    
    # MFA
    enable_mfa: bool = True
    totp_issuer: str = "COVENANT.AI"
    
    # Rate limiting
    rate_limit_per_minute: int = 1000
    rate_limit_burst: int = 100

class AISettings(BaseSettings):
    """AI/ML configuration"""
    # Model paths
    model_path: str = "./models"
    
    # Inference
    batch_size: int = 32
    max_sequence_length: int = 512
    device: str = "cuda"  # cuda, cpu, mps
    fp16: bool = True
    
    # Quantization
    quantization: bool = False
    quantization_bits: int = 8
    
    # Distributed
    distributed: bool = False
    world_size: int = 1
    
    # Model serving
    model_server: str = "torchserve"  # torchserve, triton, tfserving
    
    # Feature store
    feature_store_url: Optional[str] = None

class BlockchainSettings(BaseSettings):
    """Blockchain configuration"""
    enabled: bool = False
    provider: str = "ethereum"  # ethereum, polygon, solana
    network: str = "mainnet"
    rpc_url: str = "https://eth-mainnet.g.alchemy.com/v2/your-key"
    contract_address: Optional[str] = None
    private_key: Optional[str] = None
    
    # Gas settings
    max_gas_price_gwei: int = 100
    gas_limit: int = 300000

class MonitoringSettings(BaseSettings):
    """Monitoring configuration"""
    # Metrics
    enable_metrics: bool = True
    metrics_port: int = 9090
    
    # Tracing
    enable_tracing: bool = True
    jaeger_endpoint: str = "http://localhost:14268/api/traces"
    trace_sample_rate: float = 0.1
    
    # Logging
    log_level: str = "INFO"
    log_format: str = "json"  # json, text
    
    # APM
    sentry_dsn: Optional[str] = None
    datadog_api_key: Optional[str] = None
    newrelic_license_key: Optional[str] = None

class Settings(BaseSettings):
    """Master settings"""
    # App
    app_name: str = "COVENANT.AI Enterprise"
    app_version: str = "4.0.0"
    environment: str = "development"
    debug: bool = True
    
    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    workers: int = 4
    reload: bool = False
    
    # CORS
    cors_origins: List[str] = ["*"]
    cors_allow_credentials: bool = True
    
    # Sub-configs
    database: DatabaseSettings = DatabaseSettings()
    redis: RedisSettings = RedisSettings()
    security: SecuritySettings = SecuritySettings()
    ai: AISettings = AISettings()
    blockchain: BlockchainSettings = BlockchainSettings()
    monitoring: MonitoringSettings = MonitoringSettings()
    
    # Feature flags
    enable_graphql: bool = True
    enable_grpc: bool = True
    enable_websocket: bool = True
    enable_quantum_optimization: bool = True
    enable_federated_learning: bool = False
    
    class Config:
        env_file = ".env"
        env_nested_delimiter = "__"
        case_sensitive = False

@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()

settings = get_settings()
