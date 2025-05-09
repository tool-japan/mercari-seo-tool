from flask import Flask, request, jsonify
import openai
import os
from dotenv import load_dotenv

# 環境変数の読み込み
load_dotenv()
openai.api_key = os.getenv("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")

app = Flask(__name__)

@app.route("/api/generate", methods=["POST"])
def generate_keywords():
    # フォームデータを取得
    brand = request.form.get("brand")
    model = request.form.get("model")
    color = request.form.get("color")
    category = request.form.get("category")
    size = request.form.get("size")
    image = request.files.get("image")

    # 簡単なキーワード生成ロジック（後で強化予定）
    prompt = f"ブランド: {brand}, 型番: {model}, カラー: {color}, カテゴリ: {category}, サイズ: {size} の商品に適したSEOキーワードを生成してください。"
    
    try:
        # OpenAI API 呼び出し
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=100,
            temperature=0.7
        )
        keywords = response.choices[0].text.strip()
        return jsonify({"keywords": keywords})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

