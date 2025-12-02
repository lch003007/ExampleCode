"""
routes.py - User API Routes
提供 User Context 的 API 端點
"""

from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse
from typing import Tuple

from src.contexts.user.app import (
    RegisterUserUseCase,
    LoginUserUseCase,
    ChangePasswordUseCase,
    ChangeEmailUseCase,
    GetUserUseCase,
    GetCurrentUserUseCase,
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
from src.contexts.user.infra.repositories.user_repository_impl import UserRepositoryImpl
from src.contexts.user.domain.services.user_domain_service import UserDomainService
from src.shared.api.api_wrapper import api_response_with_logging
from src.shared.api.responses import (
    success_response,
    error_response,
    combine_responses,
    get_swagger_jwt_example
)
from src.core.config import settings
from src.core.logger.logger import logger


# 創建路由器
router = APIRouter(
    prefix="/users", 
    tags=["使用者管理"],
    responses=error_response(500, "InternalServerError", "Internal server error", "內部伺服器錯誤")
)


# 依賴注入函數
def get_user_repository() -> UserRepositoryImpl:
    """取得 User Repository 依賴"""
    return UserRepositoryImpl()


def get_user_domain_service(
    user_repository: UserRepositoryImpl = Depends(get_user_repository)
) -> UserDomainService:
    """取得 User Domain Service 依賴"""
    return UserDomainService(user_repository)


def get_register_user_use_case(
    user_domain_service: UserDomainService = Depends(get_user_domain_service)
) -> RegisterUserUseCase:
    """取得 Register User Use Case 依賴"""
    return RegisterUserUseCase(user_domain_service)


def get_login_user_use_case(
    user_domain_service: UserDomainService = Depends(get_user_domain_service)
) -> LoginUserUseCase:
    """取得 Login User Use Case 依賴"""
    return LoginUserUseCase(user_domain_service)


def get_change_password_use_case(
    user_domain_service: UserDomainService = Depends(get_user_domain_service)
) -> ChangePasswordUseCase:
    """取得 Change Password Use Case 依賴"""
    return ChangePasswordUseCase(user_domain_service)


def get_change_email_use_case(
    user_domain_service: UserDomainService = Depends(get_user_domain_service)
) -> ChangeEmailUseCase:
    """取得 Change Email Use Case 依賴"""
    return ChangeEmailUseCase(user_domain_service)


def get_user_use_case(
    user_domain_service: UserDomainService = Depends(get_user_domain_service)
) -> GetUserUseCase:
    """取得 Get User Use Case 依賴"""
    return GetUserUseCase(user_domain_service)


def get_current_user_use_case(
    user_domain_service: UserDomainService = Depends(get_user_domain_service)
) -> GetCurrentUserUseCase:
    """取得 Get Current User Use Case 依賴"""
    return GetCurrentUserUseCase(user_domain_service)


@router.post(
    "/register",
    summary="註冊使用者",
    description="建立新的使用者帳號",
    response_description="註冊成功後返回使用者基本資訊",
    responses=combine_responses(
        success_response(
            {"id": 1, "username": "alice", "email": "alice@example.com"},
            "註冊成功"
        ),
        error_response(409, "UsernameAlreadyExistsError", "Username 'alice' already exists", "使用者名稱或 Email 已存在"),
        error_response(422, "ValidationError", "Invalid input data", "輸入資料驗證失敗")
    )
)
async def register_user(
    request: Request,
    input_dto: RegisterUserInputDTO,
    register_use_case: RegisterUserUseCase = Depends(get_register_user_use_case)
):
    """
    註冊使用者
    
    建立新的使用者帳號，需要提供使用者名稱、密碼，Email 為可選。
    
    - **username**: 使用者名稱（必填，3-50 字元）
    - **password**: 密碼（必填，至少 8 字元）
    - **email**: Email 地址（可選，需符合 Email 格式）
    """
    try:
        logger.api_info("POST", "/users/register", username=input_dto.username)
        
        # 呼叫 Use Case
        result = register_use_case.execute(input_dto)
        
        # 使用 API 回應包裝器
        return api_response_with_logging(result.model_dump(), request)
        
    except Exception as e:
        logger.api_error("RegisterUserError", str(e))
        return api_response_with_logging(e, request)


@router.post(
    "/login",
    summary="使用者登入",
    description="使用使用者名稱和密碼進行登入，成功後返回 JWT token",
    response_description="登入成功後返回 JWT token 資訊",
    responses=combine_responses(
        success_response(
            {
                "access_token": get_swagger_jwt_example(),
                "refresh_token": get_swagger_jwt_example(),
                "expires_in": settings.security.jwt_expire_seconds
            },
            "登入成功"
        ),
        error_response(401, "InvalidCredentialsError", "Invalid username or password", "使用者名稱或密碼錯誤"),
        error_response(422, "ValidationError", "Invalid input data", "輸入資料驗證失敗")
    )
)
async def login_user(
    request: Request,
    input_dto: LoginUserInputDTO,
    login_use_case: LoginUserUseCase = Depends(get_login_user_use_case)
):
    """
    使用者登入
    
    使用使用者名稱和密碼進行登入驗證，成功後返回 JWT token 用於後續 API 呼叫。
    
    - **username**: 使用者名稱（必填）
    - **password**: 密碼（必填）
    """
    try:
        logger.api_info("POST", "/users/login", username=input_dto.username)
        
        # 呼叫 Use Case
        result = login_use_case.execute(input_dto)
        
        # 使用 API 回應包裝器
        return api_response_with_logging(result.model_dump(), request)
        
    except Exception as e:
        logger.api_error("LoginUserError", str(e))
        return api_response_with_logging(e, request)


@router.get(
    "/me",
    summary="查詢當前登入者",
    description="根據 JWT token 查詢當前登入使用者的資訊",
    response_description="返回當前登入使用者的詳細資訊",
    responses=combine_responses(
        success_response(
            {
                "id": 1,
                "username": "alice",
                "email": "alice@example.com",
                "roles": ["user"]
            },
            "查詢成功"
        ),
        error_response(401, "MissingTokenError", "Missing Authorization header", "JWT token 無效或過期")
    ),
    dependencies=[]  # 這裡會由 middleware 處理認證
)
async def get_current_user(
    request: Request,
    get_current_user_use_case: GetCurrentUserUseCase = Depends(get_current_user_use_case)
):
    """
    查詢當前登入者
    
    根據請求中的 JWT token 查詢當前登入使用者的詳細資訊。
    需要在請求 header 中包含有效的 Authorization token。
    
    **認證要求**: 需要在 Authorization header 中提供有效的 JWT token
    
    **使用步驟**:
    1. 先調用 `/users/login` 端點獲取 JWT token
    2. 在 Swagger UI 中點擊右上角的 "Authorize" 按鈕
    3. 輸入 JWT token（不需要 "Bearer " 前綴）
    4. 然後調用此端點
    """
    try:
        logger.api_info("GET", "/users/me")
        
        # 從 middleware 中取得用戶資訊
        user_info = getattr(request.state, 'user', None)
        if not user_info:
            from src.shared.errors.system_error.auth_error import MissingTokenError
            raise MissingTokenError("Missing Authorization header")
        
        user_id = user_info.get('user_id')
        if not user_id:
            from src.shared.errors.system_error.auth_error import MissingTokenError
            raise MissingTokenError("Invalid user information")
        
        # 轉換 user_id 為整數
        try:
            user_id_int = int(user_id)
        except (ValueError, TypeError):
            from src.shared.errors.system_error.auth_error import MissingTokenError
            raise MissingTokenError("Invalid user ID format")
        
        logger.api_info("GET", "/users/me", user_id=str(user_id_int))
        
        # 呼叫 Use Case
        result = get_current_user_use_case.execute(user_id_int)
        
        # 使用 API 回應包裝器
        return api_response_with_logging(result.model_dump(), request)
        
    except Exception as e:
        logger.api_error("GetCurrentUserError", str(e))
        return api_response_with_logging(e, request)


@router.get(
    "/{user_id}",
    summary="查詢使用者資訊",
    description="根據使用者 ID 查詢特定使用者的基本資訊",
    response_description="返回指定使用者的基本資訊",
    responses=combine_responses(
        success_response(
            {
                "id": 1,
                "username": "alice",
                "email": "alice@example.com"
            },
            "查詢成功"
        ),
        error_response(404, "UserNotFoundError", "User with id 999 not found", "使用者不存在"),
        error_response(422, "ValidationError", "Invalid user ID format", "使用者 ID 格式錯誤")
    )
)
async def get_user(
    request: Request,
    user_id: int,
    get_user_use_case: GetUserUseCase = Depends(get_user_use_case)
):
    """
    查詢使用者資訊
    
    根據使用者 ID 查詢特定使用者的基本資訊。
    
    - **user_id**: 使用者 ID（必填，整數）
    """
    try:
        logger.api_info("GET", f"/users/{user_id}", user_id=str(user_id))
        
        # 建立輸入 DTO
        input_dto = GetUserInputDTO(id=user_id)
        
        # 呼叫 Use Case
        result = get_user_use_case.execute(input_dto)
        
        # 使用 API 回應包裝器
        return api_response_with_logging(result.model_dump(), request)
        
    except Exception as e:
        logger.api_error("GetUserError", str(e))
        return api_response_with_logging(e, request)


@router.put(
    "/{user_id}/password",
    summary="修改密碼",
    description="修改指定使用者的密碼",
    response_description="返回密碼修改結果",
    responses=combine_responses(
        success_response(
            {"message": "Password updated successfully"},
            "密碼修改成功"
        ),
        error_response(400, "InvalidPasswordError", "Invalid old password", "舊密碼錯誤"),
        error_response(404, "UserNotFoundError", "User with id 999 not found", "使用者不存在"),
        error_response(422, "ValidationError", "Invalid input data", "輸入資料驗證失敗")
    )
)
async def change_password(
    request: Request,
    user_id: int,
    input_dto: ChangePasswordInputDTO,
    change_password_use_case: ChangePasswordUseCase = Depends(get_change_password_use_case)
):
    """
    修改密碼
    
    修改指定使用者的密碼，需要提供舊密碼和新密碼。
    
    - **user_id**: 使用者 ID（必填，整數）
    - **old_password**: 舊密碼（必填）
    - **new_password**: 新密碼（必填，至少 8 字元）
    """
    try:
        logger.api_info("PUT", f"/users/{user_id}/password", user_id=str(user_id))
        
        # 呼叫 Use Case
        result = change_password_use_case.execute(user_id, input_dto)
        
        # 使用 API 回應包裝器
        return api_response_with_logging(result.model_dump(), request)
        
    except Exception as e:
        logger.api_error("ChangePasswordError", str(e))
        return api_response_with_logging(e, request)


@router.put(
    "/{user_id}/email",
    summary="修改 Email",
    description="修改指定使用者的 Email 地址",
    response_description="返回 Email 修改結果",
    responses=combine_responses(
        success_response(
            {
                "id": 1,
                "username": "alice",
                "email": "alice.new@example.com"
            },
            "Email 修改成功"
        ),
        error_response(409, "EmailAlreadyExistsError", "Email 'alice.new@example.com' already exists", "Email 已被其他使用者使用"),
        error_response(404, "UserNotFoundError", "User with id 999 not found", "使用者不存在"),
        error_response(422, "ValidationError", "Invalid email format", "輸入資料驗證失敗")
    )
)
async def change_email(
    request: Request,
    user_id: int,
    input_dto: ChangeEmailInputDTO,
    change_email_use_case: ChangeEmailUseCase = Depends(get_change_email_use_case)
):
    """
    修改 Email
    
    修改指定使用者的 Email 地址，新 Email 不能與其他使用者重複。
    
    - **user_id**: 使用者 ID（必填，整數）
    - **new_email**: 新的 Email 地址（必填，需符合 Email 格式）
    """
    try:
        logger.api_info("PUT", f"/users/{user_id}/email", user_id=str(user_id), new_email=input_dto.new_email)
        
        # 呼叫 Use Case
        result = change_email_use_case.execute(user_id, input_dto)
        
        # 使用 API 回應包裝器
        return api_response_with_logging(result.model_dump(), request)
        
    except Exception as e:
        logger.api_error("ChangeEmailError", str(e))
        return api_response_with_logging(e, request)