"""
change_email_dto.py - 修改 Email DTO
定義修改 Email 的輸入和輸出 DTO
"""

from pydantic import BaseModel, Field, EmailStr


class ChangeEmailInputDTO(BaseModel):
    """
    修改 Email 輸入 DTO
    
    對應規格：
    { "new_email": "alice.new@example.com" }
    """
    new_email: EmailStr = Field(..., description="新的電子郵件地址")
    
    class Config:
        json_schema_extra = {
            "example": {
                "new_email": "alice.new@example.com"
            }
        }


class ChangeEmailOutputDTO(BaseModel):
    """
    修改 Email 輸出 DTO
    
    對應規格：
    { "id": 1, "username": "alice", "email": "alice.new@example.com" }
    """
    id: int = Field(..., description="使用者 ID")
    username: str = Field(..., description="使用者名稱")
    email: str = Field(..., description="新的電子郵件地址")
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "username": "alice",
                "email": "alice.new@example.com"
            }
        }
