"""
user_app_errors.py - User Context Application 層錯誤
定義 Use Case 專用的錯誤類別
"""

from src.shared.errors.app_error.app_error import AppError
from src.shared.errors.app_error.conflict_error import ConflictError
from src.shared.errors.system_error.auth_error import AuthError


class UsernameAlreadyExistsError(ConflictError):
    """
    使用者名稱已存在錯誤
    
    對應規格：UsernameAlreadyExistsError (409)
    """
    def __init__(self, message: str = "Username already exists", details=None):
        super().__init__(message, details)


class InvalidCredentialsError(AuthError):
    """
    無效憑證錯誤
    
    對應規格：InvalidCredentialsError (401)
    """
    def __init__(self, message: str = "Invalid credentials", details=None):
        super().__init__(message, details)


class UserNotAuthorizedError(AuthError):
    """
    使用者未授權錯誤
    
    對應規格：UserNotAuthorizedError (401)
    """
    def __init__(self, message: str = "User not authorized", details=None):
        super().__init__(message, details)
