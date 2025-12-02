"""
login_user_use_case.py - 登入使用者 Use Case
實作登入使用者的業務邏輯
"""

from src.contexts.user.app.dtos.login_user_dto import LoginUserInputDTO, LoginUserOutputDTO
from src.contexts.user.app.errors import InvalidCredentialsError
from src.contexts.user.domain.services.user_domain_service import UserDomainService
from src.contexts.user.domain.errors import UserNotFoundError, InvalidPasswordError
from src.core.logger.logger import logger


class LoginUserUseCase:
    """
    登入使用者 Use Case
    
    流程：
    1. UserRepository 查找使用者
    2. 驗證密碼
    3. 產生 access_token + refresh_token
    
    錯誤：
    - UserNotFoundError (404)
    - InvalidPasswordError (422)
    - InvalidCredentialsError (401)
    """
    
    def __init__(self, user_domain_service: UserDomainService):
        """
        初始化 LoginUserUseCase
        
        Args:
            user_domain_service: 使用者領域服務
        """
        self.user_domain_service = user_domain_service
    
    def execute(self, input_dto: LoginUserInputDTO) -> LoginUserOutputDTO:
        """
        執行登入使用者流程
        
        Args:
            input_dto: 登入使用者輸入 DTO
            
        Returns:
            LoginUserOutputDTO: 登入使用者輸出 DTO
            
        Raises:
            UserNotFoundError: 使用者不存在
            InvalidPasswordError: 密碼錯誤
            InvalidCredentialsError: 無效憑證
        """
        logger.info(f"LoginUserUseCase.execute - username={input_dto.username}")
        
        try:
            # 使用 Domain Service 認證使用者
            user = self.user_domain_service.authenticate_user(
                username_or_email=input_dto.username,
                password=input_dto.password
            )
            
            # 創建新的 JWT handler 實例，確保使用最新的配置
            from src.core.security.jwt.jwt_handler import JWTHandler
            jwt_handler = JWTHandler()
            
            # 產生 JWT Token
            access_token = jwt_handler.encode(
                user_id=str(user.id),
                roles=[user.role]  # 轉換為列表
            )
            
            # 產生 Refresh Token（簡化實作，使用相同的 token）
            refresh_token = jwt_handler.encode(
                user_id=str(user.id),
                roles=[user.role]  # 轉換為列表
            )
            
            # 轉換為輸出 DTO
            output_dto = LoginUserOutputDTO(
                access_token=access_token,
                refresh_token=refresh_token,
                expires_in=3600  # 1 小時
            )
            
            logger.info(f"LoginUserUseCase.execute - success user_id={user.id}")
            return output_dto
            
        except UserNotFoundError as e:
            logger.error(f"LoginUserUseCase.execute - UserNotFoundError: {e}")
            raise InvalidCredentialsError("Invalid username or password")
            
        except InvalidPasswordError as e:
            logger.error(f"LoginUserUseCase.execute - InvalidPasswordError: {e}")
            raise InvalidCredentialsError("Invalid username or password")
            
        except Exception as e:
            logger.error(f"LoginUserUseCase.execute - unexpected error: {e}")
            raise InvalidCredentialsError("Login failed")
