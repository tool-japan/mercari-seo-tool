from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
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

app = Flask(__name__, static_folder="../frontend")
CORS(app)

@app.route("/", methods=["GET"])
def index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/<path:filename>")
def static_files(filename):
    return send_from_directory(app.static_folder, filename)

@app.route("/api/generate", methods=["POST"])
def generate_keywords():
    try:
        # フォームデータを取得
        print("📥 フォームデータ取得開始")
        brand = request.form.get("brand")
        model = request.form.get("model")
        color = request.form.get("color")
        category = request.form.get("category")
        size = request.form.get("size")
        
        # 画像アップロードを一時的に無効化
        # image = request.files.get("image")
        # if image is None:
        #     raise Exception("画像ファイルがアップロードされていません。")

        # 必須項目のチェック
        if not all([brand, model, color, category]):
            raise Exception("フォームの入力が不完全です。")

        # キーワード生成用プロンプト
        prompt = f"ブランド: {brand}, 型番: {model}, カラー: {color}, カテゴリ: {category}, サイズ: {size} の商品に適したSEOキーワードを生成してください。"
        print(f"📢 プロンプト: {prompt}")
        
        # OpenAI Chat API 呼び出し
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "あなたは優れたSEOキーワード生成エキスパートです。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=100,
                temperature=0.7
            )
            print("✅ OpenAI API呼び出し成功")
        except Exception as api_error:
            # OpenAI APIのエラーログ
            error_message = f"🚨 OpenAI APIリクエストエラー: {api_error}\n{traceback.format_exc()}"
            print(error_message)
            return jsonify({"error": error_message}), 500

        keywords = response.choices[0].message.content.strip()
        print(f"✅ 生成されたキーワード: {keywords}")
        return jsonify({"keywords": keywords})

    except Exception as e:
        # その他のエラーログ
        error_message = f"🚨 サーバー内部エラーログ: {e}\n{traceback.format_exc()}"
        print(error_message)
        return jsonify({"error": error_message}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
