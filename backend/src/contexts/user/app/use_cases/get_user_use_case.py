"""
get_user_use_case.py - 查詢使用者資訊 Use Case
實作查詢使用者資訊的業務邏輯
"""

from src.contexts.user.app.dtos.get_user_dto import GetUserInputDTO, GetUserOutputDTO
from src.contexts.user.domain.services.user_domain_service import UserDomainService
from src.contexts.user.domain.errors import UserNotFoundError
from src.core.logger.logger import logger


class GetUserUseCase:
    """
    查詢使用者資訊 Use Case
    
    流程：
    1. UserRepository.find_by_id(id)
    2. 若不存在 → UserNotFoundError
    
    錯誤：
    - UserNotFoundError (404)
    """
    
    def __init__(self, user_domain_service: UserDomainService):
        """
        初始化 GetUserUseCase
        
        Args:
            user_domain_service: 使用者領域服務
        """
        self.user_domain_service = user_domain_service
    
    def execute(self, input_dto: GetUserInputDTO) -> GetUserOutputDTO:
        """
        執行查詢使用者資訊流程
        
        Args:
            input_dto: 查詢使用者資訊輸入 DTO
            
        Returns:
            GetUserOutputDTO: 查詢使用者資訊輸出 DTO
            
        Raises:
            UserNotFoundError: 使用者不存在
        """
        logger.info(f"GetUserUseCase.execute - user_id={input_dto.id}")
        
        try:
            # 使用 Domain Service 查詢使用者
            user = self.user_domain_service.get_user_by_id(input_dto.id)
            
            # 轉換為輸出 DTO
            output_dto = GetUserOutputDTO(
                id=user.id,
                username=user.username,
                email=user.email.value if user.email else None
            )
            
            logger.info(f"GetUserUseCase.execute - success user_id={user.id}")
            return output_dto
            
        except UserNotFoundError as e:
            logger.error(f"GetUserUseCase.execute - UserNotFoundError: {e}")
            raise
            
        except Exception as e:
            logger.error(f"GetUserUseCase.execute - unexpected error: {e}")
            raise
