from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
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
        # フォームデータの取得
        print("📥 フォームデータ取得開始")
        form_data = request.form.to_dict()
        print(f"📄 受信したフォームデータ: {form_data}")

        # 必須項目のチェック
        if not all([form_data.get("brand"), form_data.get("model"), form_data.get("color"), form_data.get("category")]):
            raise Exception("フォームの入力が不完全です。")

        # ダミー応答
        return jsonify({"keywords": "これはテスト用のダミーキーワードです！"})

    except Exception as e:
        # その他のエラーログ
        error_message = f"🚨 サーバー内部エラーログ: {e}\n{traceback.format_exc()}"
        print(error_message)
        return jsonify({"error": error_message}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
