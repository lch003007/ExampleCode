"""
run_user_api_tests.py - User API 測試運行器
運行 User API 的 E2E 和 Swagger 測試
"""

import subprocess
import sys
import os
from pathlib import Path

# 添加項目根目錄到 Python 路徑
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))


def run_e2e_tests():
    """運行 E2E 測試"""
    print("🧪 開始運行 User API E2E 測試")
    print("=" * 60)

    try:
        # 運行 E2E 測試
        result = subprocess.run([
            sys.executable, "-m", "pytest",
            "test_user_api_e2e.py",
            "-v", "--tb=short", "--color=yes"
        ], capture_output=True, text=True, cwd=Path(__file__).parent)

        print("E2E 測試輸出:")
        print(result.stdout)

        if result.stderr:
            print("E2E 測試錯誤:")
            print(result.stderr)

        if result.returncode == 0:
            print("✅ User API E2E 測試通過")
            return True
        else:
            print(f"❌ User API E2E 測試失敗 (退出碼: {result.returncode})")
            return False

    except Exception as e:
        print(f"❌ 運行 E2E 測試時發生錯誤: {e}")
        return False


def run_swagger_tests():
    """運行 Swagger 測試"""
    print("📚 開始運行 User API Swagger 測試")
    print("=" * 60)

    try:
        # 運行 Swagger 測試
        result = subprocess.run([
            sys.executable, "-m", "pytest",
            "test_user_api_swagger.py",
            "-v", "--tb=short", "--color=yes"
        ], capture_output=True, text=True, cwd=Path(__file__).parent)

        print("Swagger 測試輸出:")
        print(result.stdout)

        if result.stderr:
            print("Swagger 測試錯誤:")
            print(result.stderr)

        if result.returncode == 0:
            print("✅ User API Swagger 測試通過")
            return True
        else:
            print(f"❌ User API Swagger 測試失敗 (退出碼: {result.returncode})")
            return False

    except Exception as e:
        print(f"❌ 運行 Swagger 測試時發生錯誤: {e}")
        return False


def run_all_tests():
    """運行所有測試"""
    print("🚀 開始運行 User API 完整測試套件")
    print("=" * 80)

    e2e_success = run_e2e_tests()
    print("\n" + "=" * 60)
    swagger_success = run_swagger_tests()

    print("\n" + "=" * 80)
    print("📊 測試結果總結:")
    print("=" * 80)
    if e2e_success:
        print("✅ E2E 測試: 通過")
    else:
        print("❌ E2E 測試: 失敗")

    if swagger_success:
        print("✅ Swagger 測試: 通過")
    else:
        print("❌ Swagger 測試: 失敗")

    if e2e_success and swagger_success:
        print("\n🎉 所有 User API 測試通過！")
        return True
    else:
        print("\n💥 部分 User API 測試失敗！")
        return False


def run_specific_test(test_name):
    """運行特定測試"""
    print(f"🎯 開始運行特定測試: {test_name}")
    print("=" * 60)

    test_files = {
        "e2e": "test_user_api_e2e.py",
        "swagger": "test_user_api_swagger.py"
    }

    if test_name not in test_files:
        print(f"❌ 未知的測試名稱: {test_name}")
        print(f"可用的測試: {list(test_files.keys())}")
        return False

    try:
        result = subprocess.run([
            sys.executable, "-m", "pytest",
            test_files[test_name],
            "-v", "--tb=short", "--color=yes"
        ], capture_output=True, text=True, cwd=Path(__file__).parent)

        print(f"{test_name.upper()} 測試輸出:")
        print(result.stdout)

        if result.stderr:
            print(f"{test_name.upper()} 測試錯誤:")
            print(result.stderr)

        if result.returncode == 0:
            print(f"✅ User API {test_name.upper()} 測試通過")
            return True
        else:
            print(f"❌ User API {test_name.upper()} 測試失敗 (退出碼: {result.returncode})")
            return False

    except Exception as e:
        print(f"❌ 運行 {test_name.upper()} 測試時發生錯誤: {e}")
        return False


def main():
    """主函數"""
    if len(sys.argv) > 1:
        test_name = sys.argv[1].lower()
        run_specific_test(test_name)
    else:
        run_all_tests()


if __name__ == "__main__":
    main()
