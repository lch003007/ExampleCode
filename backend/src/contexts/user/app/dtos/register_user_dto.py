"""
register_user_dto.py - 註冊使用者 DTO
定義註冊使用者的輸入和輸出 DTO
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional


class RegisterUserInputDTO(BaseModel):
    """
    註冊使用者輸入 DTO
    
    對應規格：
    {
      "username": "alice",
      "password": "secure123",
      "email": "alice@example.com"   // optional
    }
    """
    username: str = Field(..., min_length=3, max_length=50, description="使用者名稱")
    password: str = Field(..., min_length=6, max_length=128, description="密碼")
    email: Optional[EmailStr] = Field(None, description="電子郵件地址（可選）")
    
    class Config:
        json_schema_extra = {
            "example": {
                "username": "alice",
                "password": "secure123",
                "email": "alice@example.com"
            }
        }


class RegisterUserOutputDTO(BaseModel):
    """
    註冊使用者輸出 DTO
    
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
