from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import openai
import os
from dotenv import load_dotenv
import traceback

# 環境変数の読み込み
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# デバッグメッセージ
print(f"✅ APIキーの一部: {api_key[:5]}...（一部表示）")

# OpenAI APIキーの設定
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
        brand = request.form.get("brand")
        model = request.form.get("model")
        color = request.form.get("color")
        category = request.form.get("category")
        size = request.form.get("size")
        image = request.files.get("image")

        # デバッグメッセージ
        print(f"📝 ブランド: {brand}, 型番: {model}, カラー: {color}, カテゴリ: {category}, サイズ: {size}")
        print(f"🖼️ 画像: {image}")

        # 必須項目のチェック
        if not all([brand, model, color, category]):
            raise Exception("フォームの入力が不完全です。")

        # 画像が正しくアップロードされているか確認
        if image is None:
            raise Exception("画像ファイルがアップロードされていません。")

        # キーワード生成用プロンプト
        prompt = f"ブランド: {brand}, 型番: {model}, カラー: {color}, カテゴリ: {category}, サイズ: {size} の商品に適したSEOキーワードを生成してください。"
        print(f"📢 プロンプト: {prompt}")
        
        # OpenAI API 呼び出し
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "あなたは優れたSEOキーワード生成エキスパートです。"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=100,
            temperature=0.7
        )

        keywords = response.choices[0].message.content.strip()
        print(f"✅ 生成されたキーワード: {keywords}")
        return jsonify({"keywords": keywords})

    except Exception as e:
        # エラーメッセージを表示
        error_message = f"🚨 APIリクエストエラー: {e}\n{traceback.format_exc()}"
        print(error_message)
        return jsonify({"error": error_message}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
