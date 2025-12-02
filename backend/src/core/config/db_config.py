"""
db_config.py - 資料庫相關設定
管理 PostgreSQL 資料庫連線設定
"""

from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class DatabaseConfig(BaseSettings):
    """
    資料庫設定類別
    管理 PostgreSQL 資料庫連線設定
    """
    
    # 資料庫連線設定
    host: str = Field(default="localhost", env="DB_HOST")
    port: int = Field(default=5432, env="DB_PORT")
    user: str = Field(default="postgres", env="DB_USER")
    password: str = Field(default="postgres", env="DB_PASSWORD")
    name: str = Field(default="base_project", env="DB_NAME")
    
    # 連線池設定
    pool_size: int = Field(default=10, env="DB_POOL_SIZE")
    max_overflow: int = Field(default=20, env="DB_MAX_OVERFLOW")
    pool_timeout: int = Field(default=30, env="DB_POOL_TIMEOUT")
    pool_recycle: int = Field(default=3600, env="DB_POOL_RECYCLE")
    
    # 其他設定
    echo: bool = Field(default=False, env="DB_ECHO")
    echo_pool: bool = Field(default=False, env="DB_ECHO_POOL")
    
    @property
    def database_url(self) -> str:
        """
        組合資料庫連線字串
        
        Returns:
            PostgreSQL 連線字串
        """
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"
    
    @property
    def async_database_url(self) -> str:
        """
        組合異步資料庫連線字串
        
        Returns:
            PostgreSQL 異步連線字串
        """
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"
