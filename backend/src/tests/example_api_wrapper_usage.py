"""
example_api_wrapper_usage.py - API Wrapper 使用範例
展示如何在 FastAPI Controller 中使用 API Wrapper
"""

import os
import sys

# 添加專案根目錄到 Python 路徑
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def example_controller_usage():
    """展示 Controller 中使用 API Wrapper 的範例"""
    print("=== API Wrapper 使用範例 ===")
    
    try:
        # 設定測試環境變數
        os.environ.setdefault('JWT_SECRET', 'test-secret-key-for-example')
        os.environ.setdefault('DB_HOST', 'localhost')
        os.environ.setdefault('DB_PORT', '5432')
        os.environ.setdefault('DB_USER', 'postgres')
        os.environ.setdefault('DB_PASSWORD', 'postgres')
        os.environ.setdefault('DB_NAME', 'language_path_test')
        
        from src.shared.api.api_wrapper import api_response
        from src.contexts.user.app import (
            RegisterUserUseCase,
            LoginUserUseCase,
            RegisterUserInputDTO,
            LoginUserInputDTO
        )
        from src.contexts.user.infra.repositories.user_repository_impl import UserRepositoryImpl
        from src.contexts.user.domain.services.user_domain_service import UserDomainService
        
        # 建立依賴
        user_repository = UserRepositoryImpl()
        user_domain_service = UserDomainService(user_repository)
        register_use_case = RegisterUserUseCase(user_domain_service)
        login_use_case = LoginUserUseCase(user_domain_service)
        
        print("✅ 依賴建立成功")
        
        # 模擬 Controller 函數
        def register_user_controller(input_dto: RegisterUserInputDTO):
            """模擬註冊使用者 Controller"""
            print(f"\n📝 Controller: 註冊使用者 - {input_dto.username}")
            
            try:
                # 呼叫 Use Case
                result = register_use_case.execute(input_dto)
                
                # 使用 API Wrapper 包裝回應
                response_data, status_code = api_response(result)
                
                print(f"✅ 成功回應: {response_data}")
                print(f"📊 狀態碼: {status_code}")
                
                return response_data, status_code
                
            except Exception as e:
                # 使用 API Wrapper 處理錯誤
                response_data, status_code = api_response(e)
                
                print(f"❌ 錯誤回應: {response_data}")
                print(f"📊 狀態碼: {status_code}")
                
                return response_data, status_code
        
        def login_user_controller(input_dto: LoginUserInputDTO):
            """模擬登入使用者 Controller"""
            print(f"\n📝 Controller: 登入使用者 - {input_dto.username}")
            
            try:
                # 呼叫 Use Case
                result = login_use_case.execute(input_dto)
                
                # 使用 API Wrapper 包裝回應
                response_data, status_code = api_response(result)
                
                print(f"✅ 成功回應: Access Token 長度={len(result.access_token)}")
                print(f"📊 狀態碼: {status_code}")
                
                return response_data, status_code
                
            except Exception as e:
                # 使用 API Wrapper 處理錯誤
                response_data, status_code = api_response(e)
                
                print(f"❌ 錯誤回應: {response_data}")
                print(f"📊 狀態碼: {status_code}")
                
                return response_data, status_code
        
        # 測試成功案例
        print("\n1. 測試註冊使用者成功案例...")
        import time
        timestamp = int(time.time())
        
        register_input = RegisterUserInputDTO(
            username=f"example{timestamp}",
            password="password123",
            email=f"example{timestamp}@example.com"
        )
        
        response_data, status_code = register_user_controller(register_input)
        
        # 驗證回應格式
        assert status_code == 200, f"成功案例狀態碼錯誤: {status_code}"
        assert response_data["data"] is not None, "成功案例 data 應該不為 None"
        assert response_data["error"] is None, "成功案例 error 應該為 None"
        assert "id" in response_data["data"].__dict__, "成功案例應該包含 id"
        print("✅ 註冊成功案例格式正確")
        
        # 測試登入成功案例
        print("\n2. 測試登入使用者成功案例...")
        
        login_input = LoginUserInputDTO(
            username=f"example{timestamp}",
            password="password123"
        )
        
        response_data, status_code = login_user_controller(login_input)
        
        # 驗證回應格式
        assert status_code == 200, f"登入成功案例狀態碼錯誤: {status_code}"
        assert response_data["data"] is not None, "登入成功案例 data 應該不為 None"
        assert response_data["error"] is None, "登入成功案例 error 應該為 None"
        assert "access_token" in response_data["data"].__dict__, "登入成功案例應該包含 access_token"
        print("✅ 登入成功案例格式正確")
        
        # 測試錯誤案例
        print("\n3. 測試錯誤案例...")
        
        # 嘗試重複註冊
        duplicate_input = RegisterUserInputDTO(
            username=f"example{timestamp}",
            password="password123",
            email="different@example.com"
        )
        
        response_data, status_code = register_user_controller(duplicate_input)
        
        # 驗證錯誤回應格式
        assert status_code == 409, f"錯誤案例狀態碼錯誤: {status_code}"
        assert response_data["data"] is None, "錯誤案例 data 應該為 None"
        assert response_data["error"] is not None, "錯誤案例 error 應該不為 None"
        assert "code" in response_data["error"], "錯誤案例應該包含 code"
        assert "message" in response_data["error"], "錯誤案例應該包含 message"
        print("✅ 錯誤案例格式正確")
        
        # 測試登入錯誤案例
        print("\n4. 測試登入錯誤案例...")
        
        wrong_login_input = LoginUserInputDTO(
            username=f"example{timestamp}",
            password="wrongpassword"
        )
        
        response_data, status_code = login_user_controller(wrong_login_input)
        
        # 驗證錯誤回應格式
        assert status_code == 401, f"登入錯誤案例狀態碼錯誤: {status_code}"
        assert response_data["data"] is None, "登入錯誤案例 data 應該為 None"
        assert response_data["error"] is not None, "登入錯誤案例 error 應該不為 None"
        assert "InvalidCredentialsError" in response_data["error"]["code"], "登入錯誤案例應該包含 InvalidCredentialsError"
        print("✅ 登入錯誤案例格式正確")
        
        print("\n=== API Wrapper 使用範例完成 ===")
        return True
        
    except Exception as e:
        print(f"❌ API Wrapper 使用範例失敗: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("=== API Wrapper 使用範例 ===")
    
    success = example_controller_usage()
    
    if success:
        print("\n🎉 API Wrapper 使用範例成功！")
        print("✅ 統一回應格式正常")
        print("✅ 成功案例處理正常")
        print("✅ 錯誤案例處理正常")
        print("✅ Controller 整合正常")
        print("\n📋 使用方式總結：")
        print("1. 在 Controller 中呼叫 Use Case")
        print("2. 使用 api_response(result) 包裝成功回應")
        print("3. 使用 api_response(exception) 包裝錯誤回應")
        print("4. 統一的回應格式：{data: ..., error: null} 或 {data: null, error: {...}}")
    else:
        print("\n⚠️  API Wrapper 使用範例失敗")
        print("請檢查錯誤訊息並修正問題")
