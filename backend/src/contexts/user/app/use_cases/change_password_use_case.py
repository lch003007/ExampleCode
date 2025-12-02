"""
change_password_use_case.py - 修改密碼 Use Case
實作修改密碼的業務邏輯
"""

from src.contexts.user.app.dtos.change_password_dto import ChangePasswordInputDTO, ChangePasswordOutputDTO
from src.contexts.user.domain.services.user_domain_service import UserDomainService
from src.contexts.user.domain.errors import UserNotFoundError, InvalidPasswordError
from src.core.logger.logger import logger


class ChangePasswordUseCase:
    """
    修改密碼 Use Case
    
    流程：
    1. 找到 User
    2. 驗證舊密碼
    3. 驗證新密碼格式
    4. 更新並存回 DB
    
    錯誤：
    - UserNotFoundError (404)
    - InvalidPasswordError (422)
    """
    
    def __init__(self, user_domain_service: UserDomainService):
        """
        初始化 ChangePasswordUseCase
        
        Args:
            user_domain_service: 使用者領域服務
        """
        self.user_domain_service = user_domain_service
    
    def execute(self, user_id: int, input_dto: ChangePasswordInputDTO) -> ChangePasswordOutputDTO:
        """
        執行修改密碼流程
        
        Args:
            user_id: 使用者 ID
            input_dto: 修改密碼輸入 DTO
            
        Returns:
            ChangePasswordOutputDTO: 修改密碼輸出 DTO
            
        Raises:
            UserNotFoundError: 使用者不存在
            InvalidPasswordError: 密碼錯誤
        """
        logger.info(f"ChangePasswordUseCase.execute - user_id={user_id}")
        
        try:
            # 使用 Domain Service 修改密碼
            user = self.user_domain_service.change_user_password(
                user_id=user_id,
                old_password=input_dto.old_password,
                new_password=input_dto.new_password
            )
            
            # 轉換為輸出 DTO
            output_dto = ChangePasswordOutputDTO(
                message="Password updated successfully"
            )
            
            logger.info(f"ChangePasswordUseCase.execute - success user_id={user_id}")
            return output_dto
            
        except UserNotFoundError as e:
            logger.error(f"ChangePasswordUseCase.execute - UserNotFoundError: {e}")
            raise
            
        except InvalidPasswordError as e:
            logger.error(f"ChangePasswordUseCase.execute - InvalidPasswordError: {e}")
            raise
            
        except Exception as e:
            logger.error(f"ChangePasswordUseCase.execute - unexpected error: {e}")
            raise
