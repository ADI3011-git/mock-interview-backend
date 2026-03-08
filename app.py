from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
import base64
import io
from pypdf import PdfReader

app = Flask(__name__)
CORS(app)

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

def extract_pdf_text(base64_data):
    pdf_bytes = base64.b64decode(base64_data)
    reader = PdfReader(io.BytesIO(pdf_bytes))
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text.strip()

@app.route("/api/chat", methods=["POST"])
def chat():
    try:
        body = request.get_json()
        messages = body.get("messages", [])

        groq_messages = []
        for msg in messages:
            content = msg.get("content", "")
            if isinstance(content, str):
                groq_messages.append({"role": msg.get("role", "user"), "content": content})
            elif isinstance(content, list):
                text_parts = []
                for item in content:
                    if item.get("type") == "text":
                        text_parts.append(item["text"])
                    elif item.get("type") == "document":
                        src = item.get("source", {})
                        pdf_text = extract_pdf_text(src.get("data", ""))
                        text_parts.append(f"Here is the candidate's resume:\n{pdf_text}")
                groq_messages.append({"role": msg.get("role", "user"), "content": " ".join(text_parts)})

        response = requests.post(
            GROQ_URL,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {GROQ_API_KEY}"
            },
            json={
                "model": "llama-3.3-70b-versatile",
                "max_tokens": 1500,
                "messages": groq_messages
            }
        )

        data = response.json()
        if "error" in data:
            return jsonify({"error": data["error"]}), 500

        text = data["choices"][0]["message"]["content"]
        return jsonify({"content": [{"type": "text", "text": text}]}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
