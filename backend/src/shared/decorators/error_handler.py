"""
error_handler.py - 統一錯誤處理裝飾器
提供統一的錯誤處理模式
"""

import functools
from typing import Any, Callable, Type, Union
from src.shared.errors.base_error import BaseError
from src.core.logger.logger import logger


def handle_errors(
    error_types: Union[Type[Exception], tuple] = Exception,
    default_message: str = "An error occurred",
    log_error: bool = True
):
    """
    統一錯誤處理裝飾器
    
    Args:
        error_types: 要捕獲的錯誤類型
        default_message: 預設錯誤訊息
        log_error: 是否記錄錯誤日誌
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            try:
                return func(*args, **kwargs)
            except error_types as e:
                if log_error:
                    logger.error(f"Error in {func.__name__}: {str(e)}")
                
                # 如果是 BaseError，直接重新拋出
                if isinstance(e, BaseError):
                    raise e
                
                # 其他錯誤轉換為 SystemError
                from src.shared.errors.system_error import SystemError
                raise SystemError(default_message) from e
        
        return wrapper
    return decorator


def handle_domain_errors(func: Callable) -> Callable:
    """
    處理 Domain 層錯誤的裝飾器
    """
    return handle_errors(
        error_types=(
            Exception,  # 捕獲所有異常
        ),
        default_message="Domain operation failed",
        log_error=True
    )(func)


def handle_app_errors(func: Callable) -> Callable:
    """
    處理 App 層錯誤的裝飾器
    """
    return handle_errors(
        error_types=(
            Exception,  # 捕獲所有異常
        ),
        default_message="Application operation failed",
        log_error=True
    )(func)


def handle_infra_errors(func: Callable) -> Callable:
    """
    處理 Infra 層錯誤的裝飾器
    """
    return handle_errors(
        error_types=(
            Exception,  # 捕獲所有異常
        ),
        default_message="Infrastructure operation failed",
        log_error=True
    )(func)


def handle_api_errors(func: Callable) -> Callable:
    """
    處理 API 層錯誤的裝飾器
    """
    return handle_errors(
        error_types=(
            Exception,  # 捕獲所有異常
        ),
        default_message="API operation failed",
        log_error=True
    )(func)
