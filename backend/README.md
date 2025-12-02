# Backend Base Project

一個基於 FastAPI 和 DDD 架構的通用後端基礎專案。

## 🚀 快速開始

### 1. 環境要求

- Python 3.10+
- PostgreSQL 12+
- Git

### 2. 安裝依賴

```bash
# 創建虛擬環境
python -m venv venv

# 啟動虛擬環境
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# 安裝依賴
pip install -r requirements.txt
```

### 3. 環境配置

```bash
# 複製環境變數範例文件
cp docs/env.example .env

# 編輯 .env 文件，填入實際的配置資訊
# 必需設定：
# - DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME (資料庫連接)
# - JWT_SECRET (JWT 認證密鑰)
# 
# 可選設定（如需使用 AI Service）：
# - OPENAI_API_KEY (OpenAI API 金鑰)
```

### 4. 資料庫初始化

```bash
# 初始化資料庫（創建表、載入 seed 資料）
python -c "from src.core.db.init_db import init_db; init_db()"
```

### 5. 啟動服務

```bash
# 開發模式啟動
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 6. 訪問 API 文檔

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 📁 專案結構

此專案採用 DDD（領域驅動設計）架構，結構清晰且易於擴展：

```
src/
├── contexts/           # DDD 上下文（業務領域）
│   └── user/          # 用戶上下文（範例）
│       ├── api/       # API 層 - 處理 HTTP 請求
│       ├── app/       # 應用層 - Use Cases 業務邏輯
│       ├── domain/    # 領域層 - 核心業務邏輯和規則
│       └── infra/     # 基礎設施層 - 資料庫、外部服務
├── core/              # 核心功能（框架級別）
│   ├── config/        # 配置管理
│   ├── db/           # 資料庫連接和初始化
│   ├── logger/       # 日誌系統
│   ├── middleware/   # 中間件（認證、CORS等）
│   └── security/     # 安全功能（JWT、密碼加密）
└── shared/           # 共用功能（跨 Context 使用）
    ├── api/          # API 工具（標準化回應）
    ├── errors/       # 錯誤處理（統一異常）
    └── utils/        # 工具函數
```

### 如何添加新的業務功能

1. 在 `src/contexts/` 下創建新的 Context 目錄
2. 按照 User Context 的結構組織代碼
3. 在 `main.py` 中註冊新的路由

### 共享服務

專案提供了可重用的共享服務：

- **AI Service** - OpenAI/LangChain 整合服務
  - 基礎對話功能
  - 多種 GPT 模型支持
  - 預設專業模板（程式設計、翻譯、寫作等）
  - 對話歷史管理
  - 串流輸出
  - 實用工具（摘要、翻譯、程式碼生成等）
  - 📚 [AI Service 文檔](src/shared/services/ai/README.md)
  - 🚀 [快速開始](src/shared/services/ai/QUICKSTART.md)

## 🧪 測試

```bash
# 運行所有測試
pytest

# 運行特定測試
pytest src/tests/unit/
pytest src/tests/integration/
pytest src/tests/e2e/

# 運行測試並生成覆蓋率報告
pytest --cov=src --cov-report=html
```

## 🔧 開發工具

### 資料庫管理

```bash
# 重新初始化資料庫
python -c "from src.core.db.init_db import init_db; init_db()"

# 檢查資料庫連接
python -c "from src.core.db.connection import get_session; print('Database connected successfully')"
```

### 環境變數檢查

```bash
# 檢查配置是否正確載入
python -c "from src.core.config import settings; print(settings.database.database_url)"
```

## 📝 API 使用範例

### 註冊用戶

```bash
curl -X POST "http://localhost:8000/api/users/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123"
  }'
```

### 登入

```bash
curl -X POST "http://localhost:8000/api/users/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "password123"
  }'
```

### 獲取當前用戶（需要 JWT token）

```bash
curl -X GET "http://localhost:8000/api/users/me" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## 🔒 安全設定

- JWT 認證
- 密碼雜湊（bcrypt）
- CORS 支援
- 速率限制
- 輸入驗證

## 📊 監控和日誌

- 結構化日誌
- API 請求追蹤
- 錯誤監控
- 性能指標

## 🤝 貢獻

1. Fork 專案
2. 創建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交變更 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 開啟 Pull Request

## 📄 授權

此專案採用 MIT 授權 - 查看 [LICENSE](LICENSE) 文件了解詳情。

## 🆘 支援

如有問題，請開啟 [Issue](https://github.com/your-repo/issues) 或聯繫開發團隊。