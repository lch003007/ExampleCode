"""
run_tests.py - 測試執行腳本
執行 User Domain 層的單元測試
"""

import subprocess
import sys
import os


def run_tests():
    """執行測試"""
    print("=== 執行 User Domain 層單元測試 ===")
    
    # 設定環境變數
    env = os.environ.copy()
    env['PYTHONPATH'] = os.path.dirname(os.path.abspath(__file__))
    
    # 執行 pytest
    cmd = [
        sys.executable, "-m", "pytest",
        "tests/unit/contexts/user/domain/",
        "-v",
        "--tb=short",
        "--cov=src/contexts/user/domain",
        "--cov-report=term-missing",
        "--cov-report=html:htmlcov"
    ]
    
    try:
        result = subprocess.run(cmd, env=env, capture_output=True, text=True)
        
        print("STDOUT:")
        print(result.stdout)
        
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        
        print(f"返回碼: {result.returncode}")
        
        if result.returncode == 0:
            print("✅ 所有測試通過！")
        else:
            print("❌ 測試失敗！")
            
        return result.returncode == 0
        
    except Exception as e:
        print(f"執行測試時發生錯誤: {e}")
        return False


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
