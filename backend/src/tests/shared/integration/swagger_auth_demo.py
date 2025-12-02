#!/usr/bin/env python3
"""
Swagger 認證演示
展示如何在 Swagger UI 中測試需要 JWT 認證的端點
"""

import requests
import json

def demo_swagger_auth():
    """演示 Swagger 認證流程"""
    print("🔐 Swagger JWT 認證演示")
    print("=" * 50)
    
    from src.core.config import settings
    base_url = settings.test.test_base_url
    
    # 步驟 1: 註冊用戶
    print("\n1️⃣ 註冊測試用戶...")
    register_data = {
        "username": "swaggerdemo",
        "password": "password123",
        "email": "swaggerdemo@example.com"
    }
    
    try:
        response = requests.post(f"{base_url}/users/register", json=register_data)
        if response.status_code == 200:
            user_data = response.json()["data"]
            print(f"✅ 用戶註冊成功 - ID: {user_data['id']}")
        else:
            print(f"ℹ️ 用戶可能已存在，繼續使用現有用戶")
    except Exception as e:
        print(f"❌ 註冊失敗: {e}")
        return
    
    # 步驟 2: 登入獲取 JWT token
    print("\n2️⃣ 登入獲取 JWT token...")
    login_data = {
        "username": "swaggerdemo",
        "password": "password123"
    }
    
    try:
        response = requests.post(f"{base_url}/users/login", json=login_data)
        if response.status_code == 200:
            login_result = response.json()["data"]
            access_token = login_result["access_token"]
            print(f"✅ 登入成功")
            print(f"🔑 Access Token: {access_token[:50]}...")
            print(f"⏰ 過期時間: {login_result['expires_in']} 秒")
        else:
            print(f"❌ 登入失敗: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ 登入失敗: {e}")
        return
    
    # 步驟 3: 測試需要認證的端點
    print("\n3️⃣ 測試需要認證的端點...")
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    try:
        response = requests.get(f"{base_url}/users/me", headers=headers)
        if response.status_code == 200:
            user_info = response.json()["data"]
            print(f"✅ 成功獲取當前用戶資訊:")
            print(f"   ID: {user_info['id']}")
            print(f"   用戶名: {user_info['username']}")
            print(f"   Email: {user_info['email']}")
        else:
            print(f"❌ 獲取用戶資訊失敗: {response.status_code}")
            print(f"   回應: {response.text}")
    except Exception as e:
        print(f"❌ 測試失敗: {e}")
    
    # 步驟 4: 展示 Swagger UI 使用方法
    print("\n4️⃣ 在 Swagger UI 中測試的方法:")
    print(f"   📖 訪問: {settings.api.full_docs_url}")
    print("   🔑 點擊右上角的 'Authorize' 按鈕")
    print(f"   📝 在 'Value' 欄位輸入: {access_token}")
    print("   ✅ 點擊 'Authorize' 確認")
    print("   🚀 現在可以測試 /users/me 端點了！")
    
    print(f"\n💡 提示:")
    print(f"   - JWT token 有效期: {login_result['expires_in']} 秒")
    print(f"   - 如果 token 過期，重新執行登入獲取新 token")
    print(f"   - 在 Swagger UI 中，不需要輸入 'Bearer ' 前綴")

if __name__ == "__main__":
    demo_swagger_auth()
