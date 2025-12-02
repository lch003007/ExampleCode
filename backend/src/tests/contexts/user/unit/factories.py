"""
factories.py - 測試工廠類別
使用 factory_boy 建立測試資料
"""

import factory
from datetime import datetime
from src.contexts.user.domain.entities.user import User
from src.contexts.user.domain.entities.value_objects import Email, PasswordHash


class EmailFactory(factory.Factory):
    """Email 值物件工廠"""
    class Meta:
        model = Email
    
    value = factory.Faker('email')


class PasswordHashFactory(factory.Factory):
    """PasswordHash 值物件工廠"""
    class Meta:
        model = PasswordHash
    
    value = factory.LazyFunction(lambda: PasswordHash.from_plain("testpassword123").value)


class UserFactory(factory.Factory):
    """User 實體工廠"""
    class Meta:
        model = User
    
    id = factory.Sequence(lambda n: n)
    username = factory.Faker('user_name')
    email = factory.SubFactory(EmailFactory)
    password_hash = factory.SubFactory(PasswordHashFactory)
    created_at = factory.LazyFunction(datetime.utcnow)
    updated_at = factory.LazyFunction(datetime.utcnow)
    is_active = True
    is_verified = False
    role = "user"
    
    @classmethod
    def create_admin(cls, **kwargs):
        """建立管理員使用者"""
        return cls(role="admin", **kwargs)
    
    @classmethod
    def create_inactive(cls, **kwargs):
        """建立停用使用者"""
        return cls(is_active=False, **kwargs)
    
    @classmethod
    def create_verified(cls, **kwargs):
        """建立已驗證使用者"""
        return cls(is_verified=True, **kwargs)
