"""
main.py - FastAPI 應用程式主入口
整合所有 API 路由和中介軟體
"""

import os
import sys
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# 添加專案根目錄到 Python 路徑
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 載入配置
from src.core.config import settings

# 導入所有 schema 以確保外鍵引用正確解析
from src.contexts.user.infra.schema.user import User

# 建立 FastAPI 應用程式
app = FastAPI(
    title=settings.api.title,
    description=settings.api.description,
    version=settings.api.version_info,
    docs_url=settings.api.docs_url,
    redoc_url=settings.api.redoc_url,
    openapi_tags=[
        {
            "name": "使用者管理",
            "description": "使用者相關的 API 操作，包括註冊、登入、查詢等"
        }
    ]
)

# 添加 JWT 認證配置到 OpenAPI
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    from fastapi.openapi.utils import get_openapi
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    
    # 添加 JWT 認證配置
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "請輸入 JWT token，Swagger UI 會自動添加 'Bearer ' 前綴"
        }
    }
    
    # 添加全局安全配置
    openapi_schema["security"] = [{"BearerAuth": []}]
    
    # 添加標籤配置
    openapi_schema["tags"] = [
        {
            "name": "使用者管理",
            "description": "使用者相關的 API 操作，包括註冊、登入、查詢等"
        }
    ]
    
    # 為需要認證的端點添加安全要求
    protected_paths = [
        "/users/me",
        "/users/{user_id}",
        "/users/{user_id}/password", 
        "/users/{user_id}/email"
    ]
    
    for path in openapi_schema["paths"]:
        for method in openapi_schema["paths"][path]:
            # 檢查是否為需要認證的端點
            if any(protected_path in path for protected_path in protected_paths):
                openapi_schema["paths"][path][method]["security"] = [{"BearerAuth": []}]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# 設定 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.security.cors_origins,
    allow_credentials=True,
    allow_methods=settings.security.cors_methods,
    allow_headers=settings.security.cors_headers,
)

# 添加認證中介軟體
from src.core.middleware.auth import AuthMiddleware
app.add_middleware(AuthMiddleware)

# 全域異常處理器
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """全域異常處理器"""
    return JSONResponse(
        status_code=500,
        content={
            "data": None,
            "error": {
                "code": "InternalServerError",
                "message": "Internal server error"
            }
        }
    )

# 健康檢查端點
@app.get(
    "/health",
    summary="健康檢查",
    description="檢查 API 服務是否正常運行",
    response_description="返回 API 服務狀態",
    responses={
        200: {
            "description": "服務正常",
            "content": {
                "application/json": {
                    "example": {
                        "data": {
                            "status": "healthy",
                            "message": "Base API is running"
                        },
                        "error": None
                    }
                }
            }
        }
    }
)
async def health_check():
    """
    健康檢查端點
    
    用於檢查 API 服務是否正常運行，通常用於負載均衡器或監控系統。
    
    返回服務狀態和運行訊息。
    """
    return {
        "data": {
            "status": "healthy",
            "message": "Base API is running"
        },
        "error": None
    }

# 包含 User API 路由
from src.contexts.user.api.routes import router as user_router
app.include_router(user_router)

# 根路徑
@app.get(
    "/",
    summary="API 根路徑",
    description="返回 API 基本資訊和文檔連結",
    response_description="返回 API 歡迎訊息和相關連結",
    responses={
        200: {
            "description": "成功返回 API 資訊",
            "content": {
                "application/json": {
                    "example": {
                        "data": {
                            "message": "Welcome to Base API",
                            "version": "1.0.0",
                            "docs": "/docs"
                        },
                        "error": None
                    }
                }
            }
        }
    }
)
async def root():
    """
    API 根路徑
    
    返回 API 的基本資訊，包括版本號和文檔連結。
    
    提供 Swagger UI 文檔的連結。
    """
    return {
        "data": {
            "message": "Welcome to Base API",
            "version": "1.0.0",
            "docs": "/docs"
        },
        "error": None
    }

if __name__ == "__main__":
    import uvicorn
    
    # 初始化資料庫
    try:
        from src.core.db.init_db import init_db
        print("正在初始化資料庫...")
        init_db()
        print("✅ 資料庫初始化完成")
    except Exception as e:
        print(f"❌ 資料庫初始化失敗: {e}")
        print("請確保 PostgreSQL 服務正在運行，並且資料庫設定正確")
    
    # 啟動伺服器
    print("\n🚀 啟動 Base API 伺服器...")
    print(f"📖 API 文件: {settings.api.full_docs_url}")
    print(f"🔍 ReDoc: http://{settings.api.host}:{settings.api.port}{settings.api.redoc_url}")
    print(f"❤️  健康檢查: http://{settings.api.host}:{settings.api.port}{settings.api.health_check_url}")
    
    uvicorn.run(
        "main:app",
        host=settings.api.host,
        port=settings.api.port,
        reload=True,
        log_level=settings.log_level.lower()
    )