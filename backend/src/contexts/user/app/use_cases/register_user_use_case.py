"""
register_user_use_case.py - 註冊使用者 Use Case
實作註冊使用者的業務邏輯
"""

from src.contexts.user.app.dtos.register_user_dto import RegisterUserInputDTO, RegisterUserOutputDTO
from src.contexts.user.app.errors import UsernameAlreadyExistsError
from src.contexts.user.domain.services.user_domain_service import UserDomainService
from src.contexts.user.domain.errors import EmailAlreadyExistsError, InvalidPasswordError, InvalidEmailFormatError
from src.core.logger.logger import logger
from src.shared.decorators import handle_app_errors


class RegisterUserUseCase:
    """
    註冊使用者 Use Case
    
    流程：
    1. 檢查 username 是否重複
    2. 檢查 password 格式
    3. 建立 User Entity（密碼 Hash）
    4. UserRepository.save(user)
    
    錯誤：
    - UsernameAlreadyExistsError (409)
    - InvalidPasswordError (422)
    """
    
    def __init__(self, user_domain_service: UserDomainService):
        """
        初始化 RegisterUserUseCase
        
        Args:
            user_domain_service: 使用者領域服務
        """
        self.user_domain_service = user_domain_service
    
    @handle_app_errors
    def execute(self, input_dto: RegisterUserInputDTO) -> RegisterUserOutputDTO:
        """
        執行註冊使用者流程
        
        Args:
            input_dto: 註冊使用者輸入 DTO
            
        Returns:
            RegisterUserOutputDTO: 註冊使用者輸出 DTO
            
        Raises:
            UsernameAlreadyExistsError: 使用者名稱已存在
            InvalidPasswordError: 密碼格式錯誤
            InvalidEmailFormatError: Email 格式錯誤
        """
        logger.info(f"RegisterUserUseCase.execute - username={input_dto.username}")
        
        try:
            # 使用 Domain Service 註冊使用者
            user = self.user_domain_service.register_user(
                username=input_dto.username,
                email=input_dto.email,
                password=input_dto.password
            )
            
            # 轉換為輸出 DTO
            output_dto = RegisterUserOutputDTO(
                id=user.id,
                username=user.username,
                email=user.email.value if user.email else None
            )
            
            logger.info(f"RegisterUserUseCase.execute - success user_id={user.id}")
            return output_dto
            
        except EmailAlreadyExistsError as e:
            # 轉換 Domain 錯誤為 App 錯誤
            if "username" in str(e).lower():
                raise UsernameAlreadyExistsError(f"Username '{input_dto.username}' already exists")
            else:
                raise UsernameAlreadyExistsError(f"Email '{input_dto.email}' already exists")
                
        except InvalidPasswordError as e:
            logger.error(f"RegisterUserUseCase.execute - InvalidPasswordError: {e}")
            raise
            
        except InvalidEmailFormatError as e:
            logger.error(f"RegisterUserUseCase.execute - InvalidEmailFormatError: {e}")
            raise
