"""
user app - User Context Application Layer
定義 Use Case 和 DTO 的統一入口
"""

from .dtos import (
    RegisterUserInputDTO,
    RegisterUserOutputDTO,
    LoginUserInputDTO,
    LoginUserOutputDTO,
    ChangePasswordInputDTO,
    ChangePasswordOutputDTO,
    ChangeEmailInputDTO,
    ChangeEmailOutputDTO,
    GetUserInputDTO,
    GetUserOutputDTO,
    GetCurrentUserOutputDTO
)

from .use_cases import (
    RegisterUserUseCase,
    LoginUserUseCase,
    ChangePasswordUseCase,
    ChangeEmailUseCase,
    GetUserUseCase,
    GetCurrentUserUseCase
)

from .errors import (
    UsernameAlreadyExistsError,
    InvalidCredentialsError,
    UserNotAuthorizedError
)

__all__ = [
    # DTOs
    "RegisterUserInputDTO",
    "RegisterUserOutputDTO",
    "LoginUserInputDTO",
    "LoginUserOutputDTO",
    "ChangePasswordInputDTO",
    "ChangePasswordOutputDTO",
    "ChangeEmailInputDTO",
    "ChangeEmailOutputDTO",
    "GetUserInputDTO",
    "GetUserOutputDTO",
    "GetCurrentUserOutputDTO",
    
    # Use Cases
    "RegisterUserUseCase",
    "LoginUserUseCase",
    "ChangePasswordUseCase",
    "ChangeEmailUseCase",
    "GetUserUseCase",
    "GetCurrentUserUseCase",
    
    # Errors
    "UsernameAlreadyExistsError",
    "InvalidCredentialsError",
    "UserNotAuthorizedError"
]
