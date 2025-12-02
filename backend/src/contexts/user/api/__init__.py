"""
user api - User Context API Layer
定義 User 相關的 API 路由
"""

from .routes import router as user_router

__all__ = [
    "user_router"
]
