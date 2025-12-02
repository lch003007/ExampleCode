"""
ai_service_example.py - AI Service 使用範例
展示如何使用 AI Service 的各種功能
"""

import asyncio
import sys
import os

# 添加專案根目錄到 Python 路徑
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.shared.services.ai import ai_service, PromptTemplates


async def example_basic_chat():
    """範例 1: 基礎對話"""
    print("=" * 60)
    print("範例 1: 基礎對話")
    print("=" * 60)
    
    response = await ai_service.chat(
        message="請用一句話介紹 FastAPI",
        model="gpt-3.5-turbo"
    )
    
    print(f"問題: 請用一句話介紹 FastAPI")
    print(f"回答: {response.message}")
    print(f"模型: {response.model}")
    print()


async def example_with_system_prompt():
    """範例 2: 使用系統提示詞"""
    print("=" * 60)
    print("範例 2: 使用系統提示詞")
    print("=" * 60)
    
    response = await ai_service.chat(
        message="寫一個 Hello World 程式",
        model="gpt-3.5-turbo",
        system_prompt="你是一個 Python 專家，請用簡潔的程式碼回答。"
    )
    
    print(f"問題: 寫一個 Hello World 程式")
    print(f"回答:\n{response.message}")
    print()


async def example_with_template():
    """範例 3: 使用預設模板"""
    print("=" * 60)
    print("範例 3: 使用預設模板")
    print("=" * 60)
    
    # 使用程式設計助手模板
    response = await ai_service.chat_with_template(
        message="實現一個 Fibonacci 數列函數",
        template_name="programming",
        model="gpt-3.5-turbo"
    )
    
    print(f"問題: 實現一個 Fibonacci 數列函數")
    print(f"回答:\n{response.message}")
    print()


async def example_conversation():
    """範例 4: 多輪對話"""
    print("=" * 60)
    print("範例 4: 多輪對話")
    print("=" * 60)
    
    # 創建對話
    conversation_id = ai_service.create_conversation()
    print(f"創建對話 ID: {conversation_id}\n")
    
    # 第一輪對話
    response1 = await ai_service.chat(
        message="我想學習 Python 的裝飾器",
        conversation_id=conversation_id,
        model="gpt-3.5-turbo"
    )
    print(f"用戶: 我想學習 Python 的裝飾器")
    print(f"AI: {response1.message[:200]}...\n")
    
    # 第二輪對話（AI 會記住前面的內容）
    response2 = await ai_service.chat(
        message="可以給我一個實際的例子嗎？",
        conversation_id=conversation_id,
        model="gpt-3.5-turbo"
    )
    print(f"用戶: 可以給我一個實際的例子嗎？")
    print(f"AI: {response2.message[:200]}...\n")
    
    # 查看對話歷史
    history = ai_service.get_conversation(conversation_id)
    print(f"對話歷史共有 {len(history.messages)} 條訊息")
    
    # 清除對話
    ai_service.delete_conversation(conversation_id)
    print(f"已刪除對話\n")


async def example_streaming():
    """範例 5: 串流輸出"""
    print("=" * 60)
    print("範例 5: 串流輸出")
    print("=" * 60)
    
    print("問題: 介紹一下 DDD 架構")
    print("回答: ", end="", flush=True)
    
    async for chunk in ai_service.stream_chat(
        message="用 3 句話介紹 DDD（領域驅動設計）架構",
        model="gpt-3.5-turbo",
        system_prompt="請用簡潔的語言回答"
    ):
        if not chunk.is_final:
            print(chunk.content, end="", flush=True)
        else:
            print("\n[完成]\n")


async def example_summarize():
    """範例 6: 文字摘要"""
    print("=" * 60)
    print("範例 6: 文字摘要")
    print("=" * 60)
    
    long_text = """
    FastAPI 是一個現代、快速（高性能）的 Web 框架，用於基於標準 Python 類型提示使用 Python 3.7+ 構建 API。
    FastAPI 的關鍵特性包括：快速：與 NodeJS 和 Go 相當的非常高的性能（感謝 Starlette 和 Pydantic）。
    最快的 Python 框架之一。快速編碼：將功能開發速度提高約 200% 至 300%。
    更少的錯誤：減少約 40% 的人為（開發人員）引起的錯誤。
    直觀：出色的編輯器支持。到處都可以自動完成。減少調試時間。
    簡單：旨在易於使用和學習。減少閱讀文檔的時間。
    簡短：最小化代碼重複。每個參數聲明的多個功能。更少的錯誤。
    健壯：獲取生產就緒的代碼。具有自動交互式文檔。
    基於標準：基於（並完全兼容）API 的開放標準：OpenAPI（以前稱為 Swagger）和 JSON Schema。
    """
    
    summary = await ai_service.summarize_text(
        text=long_text,
        max_length=100,
        model="gpt-3.5-turbo"
    )
    
    print(f"原文長度: {len(long_text)} 字")
    print(f"摘要: {summary}")
    print()


async def example_translate():
    """範例 7: 文字翻譯"""
    print("=" * 60)
    print("範例 7: 文字翻譯")
    print("=" * 60)
    
    # 英翻中
    translation = await ai_service.translate_text(
        text="Hello, how are you today?",
        target_language="繁體中文",
        model="gpt-3.5-turbo"
    )
    
    print(f"原文: Hello, how are you today?")
    print(f"翻譯: {translation}")
    print()


async def example_generate_code():
    """範例 8: 程式碼生成"""
    print("=" * 60)
    print("範例 8: 程式碼生成")
    print("=" * 60)
    
    code = await ai_service.generate_code(
        description="實現一個計算階乘的遞迴函數",
        language="Python",
        model="gpt-3.5-turbo"
    )
    
    print(f"需求: 實現一個計算階乘的遞迴函數")
    print(f"生成的程式碼:\n{code}")
    print()


async def example_extract_json():
    """範例 9: JSON 提取"""
    print("=" * 60)
    print("範例 9: JSON 提取")
    print("=" * 60)
    
    text = "張三，35 歲，住在台北市大安區，職業是軟體工程師，興趣是閱讀和旅遊"
    
    json_data = await ai_service.extract_json(
        text=text,
        schema_description="""
        請按照以下格式提取資訊：
        {
            "name": "姓名",
            "age": 年齡（數字）,
            "address": "地址",
            "occupation": "職業",
            "hobbies": ["興趣列表"]
        }
        """,
        model="gpt-3.5-turbo"
    )
    
    print(f"原文: {text}")
    print(f"提取的 JSON:\n{json_data}")
    print()


async def example_list_resources():
    """範例 10: 列出可用資源"""
    print("=" * 60)
    print("範例 10: 列出可用資源")
    print("=" * 60)
    
    # 列出可用模型
    models = ai_service.get_available_models()
    print("可用的 AI 模型:")
    for model in models:
        print(f"  - {model}")
    print()
    
    # 列出可用模板
    templates = ai_service.get_available_templates()
    print("可用的提示詞模板:")
    for name, prompt in templates.items():
        print(f"  - {name}: {prompt[:60]}...")
    print()


async def main():
    """主函數：運行所有範例"""
    print("\n🤖 AI Service 使用範例\n")
    
    # 檢查 API Key
    from src.core.config import settings
    if not settings.ai.openai_api_key:
        print("❌ 錯誤: 未設定 OPENAI_API_KEY")
        print("請在 .env 文件中設定: OPENAI_API_KEY=your-api-key")
        return
    
    print("✅ 已檢測到 OpenAI API Key\n")
    
    try:
        # 運行各個範例
        await example_basic_chat()
        await example_with_system_prompt()
        await example_with_template()
        await example_conversation()
        await example_streaming()
        await example_summarize()
        await example_translate()
        await example_generate_code()
        await example_extract_json()
        await example_list_resources()
        
        print("=" * 60)
        print("✅ 所有範例運行完成！")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ 錯誤: {str(e)}")
        print("請確認:")
        print("1. OpenAI API Key 是否正確")
        print("2. 網路連接是否正常")
        print("3. API 配額是否充足")


if __name__ == "__main__":
    # 運行範例
    asyncio.run(main())

