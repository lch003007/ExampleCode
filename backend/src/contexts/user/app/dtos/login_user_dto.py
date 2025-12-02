"""
login_user_dto.py - 登入使用者 DTO
定義登入使用者的輸入和輸出 DTO
"""

from pydantic import BaseModel, Field


class LoginUserInputDTO(BaseModel):
    """
    登入使用者輸入 DTO
    
    對應規格：
    { "username": "alice", "password": "secure123" }
    """
    username: str = Field(..., description="使用者名稱或電子郵件")
    password: str = Field(..., description="密碼")
    
    class Config:
        json_schema_extra = {
            "example": {
                "username": "alice",
                "password": "secure123"
            }
        }


class LoginUserOutputDTO(BaseModel):
    """
    登入使用者輸出 DTO
    
    對應規格：
    {
      "access_token": "jwt-token",
      "refresh_token": "refresh-token",
      "expires_in": 3600
    }
    """
    access_token: str = Field(..., description="存取權杖")
    refresh_token: str = Field(..., description="刷新權杖")
    expires_in: int = Field(..., description="權杖過期時間（秒）")
    
    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "expires_in": 3600
            }
        }
