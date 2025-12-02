"""
get_current_user_dto.py - 查詢當前登入者 DTO
定義查詢當前登入者的輸出 DTO
"""

from pydantic import BaseModel, Field
from typing import List, Optional


class GetCurrentUserOutputDTO(BaseModel):
    """
    查詢當前登入者輸出 DTO
    
    對應規格：
    { "id": "user-123", "username": "alice", "email": "alice@example.com", "roles": ["user"] }
    """
    id: int = Field(..., description="使用者 ID")
    username: str = Field(..., description="使用者名稱")
    email: Optional[str] = Field(None, description="電子郵件地址")
    roles: List[str] = Field(default_factory=list, description="使用者角色列表")
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "username": "alice",
                "email": "alice@example.com",
                "roles": ["user"]
            }
        }
