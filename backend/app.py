from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import openai
import os
from dotenv import load_dotenv

# 環境変数の読み込み
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

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
        print(f"ブランド: {brand}, 型番: {model}, カラー: {color}, カテゴリ: {category}, サイズ: {size}")
        print(f"画像: {image}")

        # OpenAI API 呼び出し
        prompt = f"ブランド: {brand}, 型番: {model}, カラー: {color}, カテゴリ: {category}, サイズ: {size} の商品に適したSEOキーワードを生成してください。"
        
        # APIキーの確認
        if not openai.api_key:
            raise Exception("OpenAI APIキーが設定されていません。")

        # OpenAI API 呼び出し
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=100,
            temperature=0.7
        )

        keywords = response.choices[0].text.strip()
        print(f"生成されたキーワード: {keywords}")
        return jsonify({"keywords": keywords})
    except Exception as e:
        # エラーメッセージを表示
        print(f"エラー: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
