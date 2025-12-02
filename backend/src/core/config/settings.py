"""
settings.py - 主設定檔
集中管理所有設定，統一入口
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field
from .db_config import DatabaseConfig
from .security_config import SecurityConfig
from .api_config import APIConfig
from .test_config import TestConfig
from .seed_config import SeedConfig
from .ai_config import AIConfig


class Settings(BaseSettings):
    """
    主設定類別
    集中管理所有設定，統一入口
    """
    
    # 環境設定
    debug: bool = Field(default=False, env="DEBUG")
    environment: str = Field(default="development", env="ENVIRONMENT")
    
    # 資料庫設定
    database: DatabaseConfig = DatabaseConfig()
    
    # 安全設定
    security: SecurityConfig = SecurityConfig()
    
    # API 設定
    api: APIConfig = APIConfig()
    
    # 測試設定
    test: TestConfig = TestConfig()
    
    # Seed 設定
    seed: SeedConfig = SeedConfig()
    
    # AI 設定
    ai: AIConfig = AIConfig()
    
    # 日誌設定
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_format: str = Field(default="json", env="LOG_FORMAT")
    
    # 其他設定
    redis_url: Optional[str] = Field(default=None, env="REDIS_URL")
    external_api_key: Optional[str] = Field(default=None, env="EXTERNAL_API_KEY")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"


# 全域設定實例
settings = Settings()
