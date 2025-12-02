"""
user.py - User 實體
定義使用者領域實體和業務邏輯
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from .value_objects import Email, PasswordHash
from ..errors import InvalidPasswordError


@dataclass
class User:
    """
    User 領域實體
    
    封裝使用者的業務邏輯和狀態變更
    """
    id: int
    username: str
    email: Email
    password_hash: PasswordHash
    created_at: datetime
    updated_at: Optional[datetime] = field(default=None)
    is_active: bool = field(default=True)
    is_verified: bool = field(default=False)
    role: str = field(default="user")
    
    @staticmethod
    def create(username: str, email: str, password: str) -> "User":
        """
        建立新的使用者實體
        
        Args:
            username: 使用者名稱
            email: 電子郵件
            password: 明文密碼
            
        Returns:
            新的 User 實體
        """
        now = datetime.utcnow()
        return User(
            id=0,  # 新實體，ID 由資料庫生成
            username=username,
            email=Email(email),
            password_hash=PasswordHash.from_plain(password),
            created_at=now,
            updated_at=now,
            is_active=True,
            is_verified=False,
            role="user"
        )
    
    def change_email(self, new_email: Optional[str]) -> None:
        """
        變更電子郵件
        
        Args:
            new_email: 新的電子郵件地址
        """
        self.email = Email(new_email)
        self.updated_at = datetime.utcnow()
    
    def change_password(self, new_password: str) -> None:
        """
        變更密碼
        
        Args:
            new_password: 新的明文密碼
        """
        self.password_hash = PasswordHash.from_plain(new_password)
        self.updated_at = datetime.utcnow()
    
    def verify_password(self, password: str) -> bool:
        """
        驗證密碼
        
        Args:
            password: 明文密碼
            
        Returns:
            是否驗證成功
            
        Raises:
            InvalidPasswordError: 密碼驗證失敗
        """
        return self.password_hash.verify(password)
    
    def activate(self) -> None:
        """啟用使用者"""
        self.is_active = True
        self.updated_at = datetime.utcnow()
    
    def deactivate(self) -> None:
        """停用使用者"""
        self.is_active = False
        self.updated_at = datetime.utcnow()
    
    def verify(self) -> None:
        """驗證使用者"""
        self.is_verified = True
        self.updated_at = datetime.utcnow()
    
    def change_role(self, new_role: str) -> None:
        """
        變更使用者角色
        
        Args:
            new_role: 新的角色
        """
        self.role = new_role
        self.updated_at = datetime.utcnow()
    
    def is_admin(self) -> bool:
        """檢查是否為管理員"""
        return self.role == "admin"
    
    def can_login(self) -> bool:
        """檢查是否可以登入"""
        return self.is_active
    
    def __str__(self) -> str:
        """字串表示"""
        return f"User(id={self.id}, username='{self.username}', email='{self.email}')"
    
    def __repr__(self) -> str:
        """詳細字串表示"""
        return (
            f"User(id={self.id}, username='{self.username}', email='{self.email}', "
            f"is_active={self.is_active}, is_verified={self.is_verified}, role='{self.role}')"
        )
