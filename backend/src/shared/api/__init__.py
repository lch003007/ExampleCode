"""
shared/api - 共用 API 模組
提供統一的 API 回應格式和錯誤處理
"""

from .api_wrapper import api_response, APIResponse
from .responses import (
    success_response,
    error_response,
    combine_responses,
    get_swagger_jwt_example
)

__all__ = [
    "api_response",
    "APIResponse",
    "success_response",
    "error_response",
    "combine_responses",
    "get_swagger_jwt_example"
]
