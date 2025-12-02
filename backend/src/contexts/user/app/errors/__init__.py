"""
user app errors - User Context Application 層錯誤
定義 Use Case 專用的錯誤類別
"""

from .user_app_errors import (
    UsernameAlreadyExistsError,
    InvalidCredentialsError,
    UserNotAuthorizedError
)

__all__ = [
    "UsernameAlreadyExistsError",
    "InvalidCredentialsError", 
    "UserNotAuthorizedError"
]
