"""
get_current_user_use_case.py - 查詢當前登入者 Use Case
實作查詢當前登入者的業務邏輯
"""

from src.contexts.user.app.dtos.get_current_user_dto import GetCurrentUserOutputDTO
from src.contexts.user.app.errors import UserNotAuthorizedError
from src.contexts.user.domain.services.user_domain_service import UserDomainService
from src.contexts.user.domain.errors import UserNotFoundError
from src.core.logger.logger import logger


class GetCurrentUserUseCase:
    """
    查詢當前登入者 Use Case
    
    流程：
    1. 從 JWT 解析 user_id
    2. UserRepository.find_by_id(user_id)
    
    錯誤：
    - UserNotAuthorizedError (401)
    - UserNotFoundError (404)
    """
    
    def __init__(self, user_domain_service: UserDomainService):
        """
        初始化 GetCurrentUserUseCase
        
        Args:
            user_domain_service: 使用者領域服務
        """
        self.user_domain_service = user_domain_service
    
    def execute(self, user_id: int) -> GetCurrentUserOutputDTO:
        """
        執行查詢當前登入者流程
        
        Args:
            user_id: 從 JWT 解析出的使用者 ID
            
        Returns:
            GetCurrentUserOutputDTO: 查詢當前登入者輸出 DTO
            
        Raises:
            UserNotAuthorizedError: 使用者未授權
            UserNotFoundError: 使用者不存在
        """
        logger.info(f"GetCurrentUserUseCase.execute - user_id={user_id}")
        
        try:
            # 驗證 user_id 是否有效
            if not user_id or user_id <= 0:
                raise UserNotAuthorizedError("Invalid user ID")
            
            # 使用 Domain Service 查詢使用者
            user = self.user_domain_service.get_user_by_id(user_id)
            
            # 轉換為輸出 DTO
            output_dto = GetCurrentUserOutputDTO(
                id=user.id,
                username=user.username,
                email=user.email.value if user.email else None,
                roles=[user.role]  # 轉換為列表
            )
            
            logger.info(f"GetCurrentUserUseCase.execute - success user_id={user.id}")
            return output_dto
            
        except UserNotFoundError as e:
            logger.error(f"GetCurrentUserUseCase.execute - UserNotFoundError: {e}")
            raise
            
        except UserNotAuthorizedError as e:
            logger.error(f"GetCurrentUserUseCase.execute - UserNotAuthorizedError: {e}")
            raise
            
        except Exception as e:
            logger.error(f"GetCurrentUserUseCase.execute - unexpected error: {e}")
            raise UserNotAuthorizedError("Failed to get current user")
