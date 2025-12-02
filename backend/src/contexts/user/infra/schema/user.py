"""
user.py - User ORM 模型
定義使用者資料表結構
符合指定的 schema 規格
"""

from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from src.core.db.connection import Base


class User(Base):
    """
    使用者模型
    
    對應資料表：users
    符合規格：
    users (
      id INTEGER PRIMARY KEY,
      username VARCHAR(100) NOT NULL UNIQUE,
      password_hash TEXT,
      email VARCHAR(100),
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
    __tablename__ = "users"
    
    # 主鍵
    id = Column(Integer, primary_key=True, index=True)
    
    # 基本資訊
    username = Column(String(100), unique=True, nullable=False)
    password_hash = Column(Text, nullable=True)
    email = Column(String(100), nullable=True)
    
    # 時間戳記
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"
