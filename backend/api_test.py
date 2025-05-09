import openai
import os
from dotenv import load_dotenv
import traceback

# 環境変数の読み込み
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# APIキーが正しく設定されているかチェック
if not api_key:
    print("🚨 OpenAI APIキーが設定されていません。")
    exit(1)

openai.api_key = api_key

# テスト用プロンプト
prompt = "これはAPI接続テストです。SEOに適したキーワードを生成してください。"

try:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "あなたは優れたSEOキーワード生成エキスパートです。"},
            {"role": "user", "content": prompt}
        ],
        max_tokens=50,
        temperature=0.7
    )
    print("✅ OpenAI API呼び出し成功")
    print("📝 APIレスポンス:", response)

except Exception as e:
    # OpenAI APIのエラーログ
    error_message = f"🚨 OpenAI APIリクエストエラー: {e}\n{traceback.format_exc()}"
    print(error_message)
