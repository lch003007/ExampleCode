"""
user_errors.py - User Context 專屬錯誤
使用共用的錯誤系統，定義 User 相關的業務錯誤
"""

from src.shared.errors.domain_error import DomainError


class UserDomainError(DomainError):
    """
    User Domain 錯誤基底類別
    所有 User 相關的業務錯誤都繼承此類別
    """
    pass


class UserNotFoundError(UserDomainError):
    """
    使用者不存在錯誤
    
    用途：查詢不存在的使用者
    狀態碼：404 Not Found
    """
    
    def __init__(self, message: str = "User not found"):
        super().__init__(message)
    
    @property
    def status_code(self) -> int:
        return 404


class EmailAlreadyExistsError(UserDomainError):
    """
    Email 已被註冊錯誤
    
    用途：嘗試註冊已存在的 Email
    狀態碼：409 Conflict
    """
    
    def __init__(self, message: str = "Email already registered"):
        super().__init__(message)
    
    @property
    def status_code(self) -> int:
        return 409


class InvalidPasswordError(UserDomainError):
    """
    密碼格式或驗證錯誤
    
    用途：密碼格式不符或驗證失敗
    狀態碼：422 Unprocessable Entity
    """
    
    def __init__(self, message: str = "Invalid password"):
        super().__init__(message)
    
    @property
    def status_code(self) -> int:
        return 422


class InvalidEmailFormatError(UserDomainError):
    """
    Email 格式錯誤
    
    用途：Email 格式不合法
    狀態碼：422 Unprocessable Entity
    """
    
    def __init__(self, message: str = "Invalid email format"):
        super().__init__(message)
    
    @property
    def status_code(self) -> int:
        return 422
