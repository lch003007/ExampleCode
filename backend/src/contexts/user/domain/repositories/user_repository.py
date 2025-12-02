"""
user_repository.py - User Repository 介面
定義 User 資料存取介面
"""

from abc import ABC, abstractmethod
from typing import Optional, List
from ..entities.user import User


class UserRepository(ABC):
    """
    User Repository 介面
    
    定義 User 實體的資料存取契約
    實作類別應該在 infra 層提供
    """
    
    @abstractmethod
    def save(self, user: User) -> User:
        """
        儲存使用者
        
        Args:
            user: 要儲存的使用者實體
            
        Returns:
            儲存後的使用者實體（包含生成的 ID）
        """
        pass
    
    @abstractmethod
    def find_by_id(self, user_id: int) -> Optional[User]:
        """
        根據 ID 查詢使用者
        
        Args:
            user_id: 使用者 ID
            
        Returns:
            找到的使用者實體，如果不存在則回傳 None
        """
        pass
    
    @abstractmethod
    def find_by_username(self, username: str) -> Optional[User]:
        """
        根據使用者名稱查詢使用者
        
        Args:
            username: 使用者名稱
            
        Returns:
            找到的使用者實體，如果不存在則回傳 None
        """
        pass
    
    @abstractmethod
    def find_by_email(self, email: str) -> Optional[User]:
        """
        根據電子郵件查詢使用者
        
        Args:
            email: 電子郵件地址
            
        Returns:
            找到的使用者實體，如果不存在則回傳 None
        """
        pass
    
    @abstractmethod
    def find_all(self, limit: Optional[int] = None, offset: Optional[int] = None) -> List[User]:
        """
        查詢所有使用者
        
        Args:
            limit: 限制筆數
            offset: 偏移量
            
        Returns:
            使用者實體列表
        """
        pass
    
    @abstractmethod
    def find_by_role(self, role: str, limit: Optional[int] = None, offset: Optional[int] = None) -> List[User]:
        """
        根據角色查詢使用者
        
        Args:
            role: 使用者角色
            limit: 限制筆數
            offset: 偏移量
            
        Returns:
            使用者實體列表
        """
        pass
    
    @abstractmethod
    def find_active_users(self, limit: Optional[int] = None, offset: Optional[int] = None) -> List[User]:
        """
        查詢啟用的使用者
        
        Args:
            limit: 限制筆數
            offset: 偏移量
            
        Returns:
            啟用的使用者實體列表
        """
        pass
    
    @abstractmethod
    def count(self) -> int:
        """
        計算使用者總數
        
        Returns:
            使用者總數
        """
        pass
    
    @abstractmethod
    def count_by_role(self, role: str) -> int:
        """
        計算指定角色的使用者數量
        
        Args:
            role: 使用者角色
            
        Returns:
            指定角色的使用者數量
        """
        pass
    
    @abstractmethod
    def exists_by_username(self, username: str) -> bool:
        """
        檢查使用者名稱是否存在
        
        Args:
            username: 使用者名稱
            
        Returns:
            是否存在
        """
        pass
    
    @abstractmethod
    def exists_by_email(self, email: str) -> bool:
        """
        檢查電子郵件是否存在
        
        Args:
            email: 電子郵件地址
            
        Returns:
            是否存在
        """
        pass
    
    @abstractmethod
    def delete(self, user_id: int) -> bool:
        """
        刪除使用者
        
        Args:
            user_id: 使用者 ID
            
        Returns:
            是否刪除成功
        """
        pass
