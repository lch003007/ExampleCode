"""
user_domain_service.py - User Domain Service
處理複雜的 User 業務邏輯，不屬於單一實體的邏輯
"""

from typing import Optional
from ..entities.user import User
from ..repositories.user_repository import UserRepository
from ..errors import (
    UserNotFoundError,
    EmailAlreadyExistsError,
    InvalidPasswordError
)


class UserDomainService:
    """
    User Domain Service
    
    處理複雜的 User 業務邏輯：
    - 使用者註冊驗證
    - 使用者認證
    - 使用者資料變更驗證
    """
    
    def __init__(self, user_repository: UserRepository):
        """
        初始化 User Domain Service
        
        Args:
            user_repository: User Repository 實例
        """
        self.user_repository = user_repository
    
    def register_user(self, username: str, email: str, password: str) -> User:
        """
        註冊新使用者
        
        Args:
            username: 使用者名稱
            email: 電子郵件
            password: 明文密碼
            
        Returns:
            新建立的使用者實體
            
        Raises:
            EmailAlreadyExistsError: Email 已被註冊
        """
        # 檢查 Email 是否已存在
        if self.user_repository.exists_by_email(email):
            raise EmailAlreadyExistsError(f"Email {email} already registered")
        
        # 檢查使用者名稱是否已存在
        if self.user_repository.exists_by_username(username):
            raise EmailAlreadyExistsError(f"Username {username} already exists")
        
        # 建立新使用者
        user = User.create(username, email, password)
        
        # 儲存使用者
        return self.user_repository.save(user)
    
    def authenticate_user(self, username_or_email: str, password: str) -> User:
        """
        認證使用者
        
        Args:
            username_or_email: 使用者名稱或電子郵件
            password: 明文密碼
            
        Returns:
            認證成功的使用者實體
            
        Raises:
            UserNotFoundError: 使用者不存在
            InvalidPasswordError: 密碼錯誤
        """
        # 根據使用者名稱或 Email 查詢使用者
        user = self._find_user_by_username_or_email(username_or_email)
        
        if not user:
            raise UserNotFoundError(f"User not found: {username_or_email}")
        
        # 檢查使用者是否啟用
        if not user.can_login():
            raise UserNotFoundError(f"User account is not active: {username_or_email}")
        
        # 驗證密碼
        if not user.verify_password(password):
            raise InvalidPasswordError("Invalid password")
        
        return user
    
    def change_user_email(self, user_id: int, new_email: str) -> User:
        """
        變更使用者電子郵件
        
        Args:
            user_id: 使用者 ID
            new_email: 新的電子郵件
            
        Returns:
            更新後的使用者實體
            
        Raises:
            UserNotFoundError: 使用者不存在
            EmailAlreadyExistsError: Email 已被其他使用者使用
        """
        # 查詢使用者
        user = self.user_repository.find_by_id(user_id)
        if not user:
            raise UserNotFoundError(f"User not found: {user_id}")
        
        # 檢查新 Email 是否已被其他使用者使用
        existing_user = self.user_repository.find_by_email(new_email)
        if existing_user and existing_user.id != user_id:
            raise EmailAlreadyExistsError(f"Email {new_email} already registered")
        
        # 變更 Email
        user.change_email(new_email)
        
        # 儲存變更
        return self.user_repository.save(user)
    
    def change_user_password(self, user_id: int, old_password: str, new_password: str) -> User:
        """
        變更使用者密碼
        
        Args:
            user_id: 使用者 ID
            old_password: 舊密碼
            new_password: 新密碼
            
        Returns:
            更新後的使用者實體
            
        Raises:
            UserNotFoundError: 使用者不存在
            InvalidPasswordError: 舊密碼錯誤
        """
        # 查詢使用者
        user = self.user_repository.find_by_id(user_id)
        if not user:
            raise UserNotFoundError(f"User not found: {user_id}")
        
        # 驗證舊密碼
        if not user.verify_password(old_password):
            raise InvalidPasswordError("Current password is incorrect")
        
        # 變更密碼
        user.change_password(new_password)
        
        # 儲存變更
        return self.user_repository.save(user)
    
    def reset_user_password(self, user_id: int, new_password: str) -> User:
        """
        重設使用者密碼（管理員功能）
        
        Args:
            user_id: 使用者 ID
            new_password: 新密碼
            
        Returns:
            更新後的使用者實體
            
        Raises:
            UserNotFoundError: 使用者不存在
        """
        # 查詢使用者
        user = self.user_repository.find_by_id(user_id)
        if not user:
            raise UserNotFoundError(f"User not found: {user_id}")
        
        # 重設密碼
        user.change_password(new_password)
        
        # 儲存變更
        return self.user_repository.save(user)
    
    def _find_user_by_username_or_email(self, username_or_email: str) -> Optional[User]:
        """
        根據使用者名稱或 Email 查詢使用者
        
        Args:
            username_or_email: 使用者名稱或電子郵件
            
        Returns:
            找到的使用者實體，如果不存在則回傳 None
        """
        # 先嘗試作為使用者名稱查詢
        user = self.user_repository.find_by_username(username_or_email)
        if user:
            return user
        
        # 再嘗試作為 Email 查詢
        user = self.user_repository.find_by_email(username_or_email)
        return user
    
    def get_user_by_id(self, user_id: int) -> User:
        """
        根據 ID 查詢使用者
        
        Args:
            user_id: 使用者 ID
            
        Returns:
            使用者實體
            
        Raises:
            UserNotFoundError: 使用者不存在
        """
        user = self.user_repository.find_by_id(user_id)
        if not user:
            raise UserNotFoundError(f"User with id {user_id} not found")
        
        return user
