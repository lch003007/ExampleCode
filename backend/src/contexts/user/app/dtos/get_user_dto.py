"""
get_user_dto.py - 查詢使用者資訊 DTO
定義查詢使用者資訊的輸入和輸出 DTO
"""

from pydantic import BaseModel, Field
from typing import Optional


class GetUserInputDTO(BaseModel):
    """
    查詢使用者資訊輸入 DTO
    
    對應規格：
    { "id": 1 }
    """
    id: int = Field(..., gt=0, description="使用者 ID")
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1
            }
        }


class GetUserOutputDTO(BaseModel):
    """
    查詢使用者資訊輸出 DTO
    
    對應規格：
    { "id": 1, "username": "alice", "email": "alice@example.com" }
    """
    id: int = Field(..., description="使用者 ID")
    username: str = Field(..., description="使用者名稱")
    email: Optional[str] = Field(None, description="電子郵件地址")
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "username": "alice",
                "email": "alice@example.com"
            }
        }
