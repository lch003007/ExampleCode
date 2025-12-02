"""
change_password_dto.py - 修改密碼 DTO
定義修改密碼的輸入和輸出 DTO
"""

from pydantic import BaseModel, Field


class ChangePasswordInputDTO(BaseModel):
    """
    修改密碼輸入 DTO
    
    對應規格：
    { "old_password": "secure123", "new_password": "newpass456" }
    """
    old_password: str = Field(..., description="舊密碼")
    new_password: str = Field(..., min_length=6, max_length=128, description="新密碼")
    
    class Config:
        json_schema_extra = {
            "example": {
                "old_password": "secure123",
                "new_password": "newpass456"
            }
        }


class ChangePasswordOutputDTO(BaseModel):
    """
    修改密碼輸出 DTO
    
    對應規格：
    { "message": "Password updated successfully" }
    """
    message: str = Field(..., description="成功訊息")
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "Password updated successfully"
            }
        }
