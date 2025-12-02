"""
change_email_use_case.py - 修改 Email Use Case
實作修改 Email 的業務邏輯
"""

from src.contexts.user.app.dtos.change_email_dto import ChangeEmailInputDTO, ChangeEmailOutputDTO
from src.contexts.user.domain.services.user_domain_service import UserDomainService
from src.contexts.user.domain.errors import UserNotFoundError, InvalidEmailFormatError, EmailAlreadyExistsError
from src.core.logger.logger import logger


class ChangeEmailUseCase:
    """
    修改 Email Use Case
    
    流程：
    1. 找到 User
    2. 驗證 email 格式
    3. 更新 email 並存回 DB
    
    錯誤：
    - UserNotFoundError (404)
    - InvalidEmailFormatError (422)
    """
    
    def __init__(self, user_domain_service: UserDomainService):
        """
        初始化 ChangeEmailUseCase
        
        Args:
            user_domain_service: 使用者領域服務
        """
        self.user_domain_service = user_domain_service
    
    def execute(self, user_id: int, input_dto: ChangeEmailInputDTO) -> ChangeEmailOutputDTO:
        """
        執行修改 Email 流程
        
        Args:
            user_id: 使用者 ID
            input_dto: 修改 Email 輸入 DTO
            
        Returns:
            ChangeEmailOutputDTO: 修改 Email 輸出 DTO
            
        Raises:
            UserNotFoundError: 使用者不存在
            InvalidEmailFormatError: Email 格式錯誤
            EmailAlreadyExistsError: Email 已存在
        """
        logger.info(f"ChangeEmailUseCase.execute - user_id={user_id} new_email={input_dto.new_email}")
        
        try:
            # 使用 Domain Service 修改 Email
            user = self.user_domain_service.change_user_email(
                user_id=user_id,
                new_email=input_dto.new_email
            )
            
            # 轉換為輸出 DTO
            output_dto = ChangeEmailOutputDTO(
                id=user.id,
                username=user.username,
                email=user.email.value if user.email else None
            )
            
            logger.info(f"ChangeEmailUseCase.execute - success user_id={user_id}")
            return output_dto
            
        except UserNotFoundError as e:
            logger.error(f"ChangeEmailUseCase.execute - UserNotFoundError: {e}")
            raise
            
        except InvalidEmailFormatError as e:
            logger.error(f"ChangeEmailUseCase.execute - InvalidEmailFormatError: {e}")
            raise
            
        except EmailAlreadyExistsError as e:
            logger.error(f"ChangeEmailUseCase.execute - EmailAlreadyExistsError: {e}")
            raise
            
        except Exception as e:
            logger.error(f"ChangeEmailUseCase.execute - unexpected error: {e}")
            raise
