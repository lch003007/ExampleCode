"""
value_objects.py - User Context 值物件
定義 Email 和 PasswordHash 值物件
"""

import re
import bcrypt
from dataclasses import dataclass
from typing import Optional
from ..errors import InvalidEmailFormatError, InvalidPasswordError


@dataclass(frozen=True)
class Email:
    """
    Email 值物件
    
    封裝 Email 的驗證邏輯和不可變性
    """
    value: Optional[str]
    
    def __post_init__(self):
        """
        驗證 Email 格式
        允許 None 值或空字串（用於可選的 Email 欄位）
        """
        if self.value is None or self.value.strip() == "":
            return  # ✅ 允許空值或空字串
        
        # 基本的 Email 格式驗證
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, self.value):
            raise InvalidEmailFormatError("Invalid email format")
        
        # 額外檢查：不能有連續的點
        if '..' in self.value:
            raise InvalidEmailFormatError("Invalid email format")
    
    def __str__(self) -> str:
        """字串表示"""
        return self.value or ""
    
    def is_empty(self) -> bool:
        """檢查是否為空"""
        return self.value is None or self.value.strip() == ""


@dataclass(frozen=True)
class PasswordHash:
    """
    密碼雜湊值物件
    
    封裝密碼雜湊的生成和驗證邏輯
    """
    value: str
    
    @staticmethod
    def from_plain(password: str) -> "PasswordHash":
        """
        從明文密碼生成雜湊
        
        Args:
            password: 明文密碼
            
        Returns:
            PasswordHash 實例
            
        Raises:
            InvalidPasswordError: 密碼格式不符
        """
        # 使用 UTF-8 編碼計算字節長度，更準確處理 Unicode 字符
        password_bytes = password.encode('utf-8')
        if len(password_bytes) < 6:
            raise InvalidPasswordError("Password must be at least 6 characters")
        
        if len(password_bytes) > 128:
            raise InvalidPasswordError("Password must be less than 128 characters")
        
        # 使用 bcrypt 生成雜湊
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        return PasswordHash(hashed.decode('utf-8'))
    
    def verify(self, plain_password: str) -> bool:
        """
        驗證明文密碼
        
        Args:
            plain_password: 明文密碼
            
        Returns:
            是否驗證成功
        """
        try:
            if not isinstance(plain_password, str):
                return False
            
            is_valid = bcrypt.checkpw(
                plain_password.encode('utf-8'), 
                self.value.encode('utf-8')
            )
            return is_valid
            
        except Exception:
            return False
    
    def __str__(self) -> str:
        """字串表示（隱藏實際雜湊值）"""
        return "***HASHED***"
