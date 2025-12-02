"""
user_repository_impl.py - User Repository 實作
使用 SQLAlchemy 實作 User Repository 介面
"""

from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from src.core.db.base import BaseRepository
from src.contexts.user.infra.schema.user import User as UserSchema
from src.contexts.user.domain.entities.user import User as UserEntity
from src.contexts.user.domain.entities.value_objects import Email, PasswordHash
from src.contexts.user.domain.repositories.user_repository import UserRepository
from src.contexts.user.domain.errors import EmailAlreadyExistsError
from src.core.logger.logger import logger


class UserRepositoryImpl(BaseRepository[UserSchema], UserRepository):
    """
    User Repository 實作
    
    繼承 BaseRepository 和實作 UserRepository 介面
    負責 User 實體的資料存取
    """
    
    def __init__(self):
        """初始化 User Repository"""
        super().__init__(UserSchema)
    
    def save(self, user: UserEntity) -> UserEntity:
        """
        儲存使用者
        
        Args:
            user: 要儲存的使用者實體
            
        Returns:
            儲存後的使用者實體（包含生成的 ID）
        """
        with self.get_session() as session:
            try:
                if user.id == 0:
                    # 新增使用者
                    user_schema = self._entity_to_schema(user)
                    session.add(user_schema)
                    session.flush()  # 獲取生成的 ID
                    
                    # 更新實體的 ID
                    user.id = user_schema.id
                    
                    logger.db_info(f"Insert success table={self.table_name} id={user.id}")
                else:
                    # 更新使用者
                    user_schema = session.query(UserSchema).filter_by(id=user.id).first()
                    if user_schema:
                        self._update_schema_from_entity(user_schema, user)
                        session.flush()
                        
                        logger.db_info(f"Update success table={self.table_name} id={user.id}")
                    else:
                        raise ValueError(f"User with id {user.id} not found")
                
                return user
                
            except IntegrityError as e:
                if "username" in str(e):
                    raise EmailAlreadyExistsError(f"Username {user.username} already exists")
                elif "email" in str(e):
                    raise EmailAlreadyExistsError(f"Email {user.email} already exists")
                else:
                    raise
    
    def find_by_id(self, user_id: int) -> Optional[UserEntity]:
        """
        根據 ID 查詢使用者
        
        Args:
            user_id: 使用者 ID
            
        Returns:
            找到的使用者實體，如果不存在則回傳 None
        """
        with self.get_session() as session:
            user_schema = session.query(UserSchema).filter_by(id=user_id).first()
            
            if user_schema:
                logger.db_info(f"Fetch by id={user_id} table={self.table_name} result=found")
                return self._schema_to_entity(user_schema)
            else:
                logger.db_info(f"Fetch by id={user_id} table={self.table_name} result=not_found")
                return None
    
    def find_by_username(self, username: str) -> Optional[UserEntity]:
        """
        根據使用者名稱查詢使用者
        
        Args:
            username: 使用者名稱
            
        Returns:
            找到的使用者實體，如果不存在則回傳 None
        """
        with self.get_session() as session:
            user_schema = session.query(UserSchema).filter_by(username=username).first()
            
            if user_schema:
                logger.db_info(f"Fetch by username={username} table={self.table_name} result=found")
                return self._schema_to_entity(user_schema)
            else:
                logger.db_info(f"Fetch by username={username} table={self.table_name} result=not_found")
                return None
    
    def find_by_email(self, email: str) -> Optional[UserEntity]:
        """
        根據電子郵件查詢使用者
        
        Args:
            email: 電子郵件地址
            
        Returns:
            找到的使用者實體，如果不存在則回傳 None
        """
        with self.get_session() as session:
            user_schema = session.query(UserSchema).filter_by(email=email).first()
            
            if user_schema:
                logger.db_info(f"Fetch by email={email} table={self.table_name} result=found")
                return self._schema_to_entity(user_schema)
            else:
                logger.db_info(f"Fetch by email={email} table={self.table_name} result=not_found")
                return None
    
    def find_all(self, limit: Optional[int] = None, offset: Optional[int] = None) -> List[UserEntity]:
        """
        查詢所有使用者
        
        Args:
            limit: 限制筆數
            offset: 偏移量
            
        Returns:
            使用者實體列表
        """
        with self.get_session() as session:
            query = session.query(UserSchema)
            
            if offset:
                query = query.offset(offset)
            if limit:
                query = query.limit(limit)
            
            user_schemas = query.all()
            users = [self._schema_to_entity(schema) for schema in user_schemas]
            
            logger.db_info(f"Query table={self.table_name} filters=None count={len(users)}")
            return users
    
    def find_by_role(self, role: str, limit: Optional[int] = None, offset: Optional[int] = None) -> List[UserEntity]:
        """
        根據角色查詢使用者
        
        注意：由於簡化的 schema 沒有 role 欄位，此方法回傳空列表
        
        Args:
            role: 使用者角色
            limit: 限制筆數
            offset: 偏移量
            
        Returns:
            使用者實體列表
        """
        # 由於簡化的 schema 沒有 role 欄位，回傳空列表
        logger.db_info(f"Query by role={role} table={self.table_name} count=0 (role not supported in simplified schema)")
        return []
    
    def find_active_users(self, limit: Optional[int] = None, offset: Optional[int] = None) -> List[UserEntity]:
        """
        查詢啟用的使用者
        
        注意：由於簡化的 schema 沒有 is_active 欄位，此方法回傳所有使用者
        
        Args:
            limit: 限制筆數
            offset: 偏移量
            
        Returns:
            啟用的使用者實體列表
        """
        # 由於簡化的 schema 沒有 is_active 欄位，回傳所有使用者
        return self.find_all(limit, offset)
    
    def count(self) -> int:
        """
        計算使用者總數
        
        Returns:
            使用者總數
        """
        with self.get_session() as session:
            count = session.query(UserSchema).count()
            logger.db_info(f"Count table={self.table_name} filters=None count={count}")
            return count
    
    def count_by_role(self, role: str) -> int:
        """
        計算指定角色的使用者數量
        
        注意：由於簡化的 schema 沒有 role 欄位，此方法回傳 0
        
        Args:
            role: 使用者角色
            
        Returns:
            指定角色的使用者數量
        """
        # 由於簡化的 schema 沒有 role 欄位，回傳 0
        logger.db_info(f"Count by role={role} table={self.table_name} count=0 (role not supported in simplified schema)")
        return 0
    
    def exists_by_username(self, username: str) -> bool:
        """
        檢查使用者名稱是否存在
        
        Args:
            username: 使用者名稱
            
        Returns:
            是否存在
        """
        with self.get_session() as session:
            exists = session.query(UserSchema).filter_by(username=username).first() is not None
            logger.db_info(f"Check username exists={exists} table={self.table_name} username={username}")
            return exists
    
    def exists_by_email(self, email: str) -> bool:
        """
        檢查電子郵件是否存在
        
        Args:
            email: 電子郵件地址
            
        Returns:
            是否存在
        """
        with self.get_session() as session:
            exists = session.query(UserSchema).filter_by(email=email).first() is not None
            logger.db_info(f"Check email exists={exists} table={self.table_name} email={email}")
            return exists
    
    def delete(self, user_id: int) -> bool:
        """
        刪除使用者
        
        Args:
            user_id: 使用者 ID
            
        Returns:
            是否刪除成功
        """
        with self.get_session() as session:
            user_schema = session.query(UserSchema).filter_by(id=user_id).first()
            if user_schema:
                session.delete(user_schema)
                session.flush()
                
                logger.db_info(f"Delete success table={self.table_name} id={user_id}")
                return True
            else:
                logger.db_info(f"Delete failed table={self.table_name} id={user_id} reason=not_found")
                return False
    
    def _entity_to_schema(self, user: UserEntity) -> UserSchema:
        """
        將 Domain 實體轉換為 ORM Schema
        
        Args:
            user: Domain 實體
            
        Returns:
            ORM Schema
        """
        return UserSchema(
            id=user.id if user.id > 0 else None,
            username=user.username,
            password_hash=user.password_hash.value if user.password_hash else None,
            email=user.email.value if user.email else None,
            created_at=user.created_at
        )
    
    def _schema_to_entity(self, user_schema: UserSchema) -> UserEntity:
        """
        將 ORM Schema 轉換為 Domain 實體
        
        Args:
            user_schema: ORM Schema
            
        Returns:
            Domain 實體
        """
        return UserEntity(
            id=user_schema.id,
            username=user_schema.username,
            email=Email(user_schema.email),
            password_hash=PasswordHash(user_schema.password_hash) if user_schema.password_hash else None,
            created_at=user_schema.created_at,
            updated_at=user_schema.created_at,  # 簡化 schema 沒有 updated_at
            is_active=True,  # 簡化 schema 沒有 is_active，預設為 True
            is_verified=False,  # 簡化 schema 沒有 is_verified，預設為 False
            role="user"  # 簡化 schema 沒有 role，預設為 "user"
        )
    
    def _update_schema_from_entity(self, user_schema: UserSchema, user: UserEntity):
        """
        從 Domain 實體更新 ORM Schema
        
        Args:
            user_schema: 要更新的 ORM Schema
            user: Domain 實體
        """
        user_schema.username = user.username
        user_schema.password_hash = user.password_hash.value if user.password_hash else None
        user_schema.email = user.email.value if user.email else None