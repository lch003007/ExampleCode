"""
seed_config.py - Seed 資料配置
管理初始資料的配置
"""

from typing import List, Dict, Any
from pydantic_settings import BaseSettings
from pydantic import Field


class SeedConfig(BaseSettings):
    """
    Seed 資料配置類別
    管理初始資料的配置
    """
    
    # 預設使用者資料
    default_users: List[Dict[str, Any]] = Field(
        default=[
            {
                "username": "admin",
                "email": "admin@languagepath.com",
                "password": "admin123",
                "role": "admin"
            },
            {
                "username": "demo_user",
                "email": "demo@languagepath.com", 
                "password": "demo123",
                "role": "user"
            },
            {
                "username": "test_user",
                "email": "test@languagepath.com",
                "password": "test123",
                "role": "user"
            }
        ],
        env="SEED_DEFAULT_USERS"
    )
    
    # 是否自動執行 seed
    auto_seed: bool = Field(default=True, env="SEED_AUTO_EXECUTE")
    
    # 是否覆蓋現有資料
    overwrite_existing: bool = Field(default=False, env="SEED_OVERWRITE_EXISTING")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"
