from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
import base64

app = Flask(__name__)
CORS(app)

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

@app.route("/api/chat", methods=["POST"])
def chat():
    try:
        body = request.get_json()
        messages = body.get("messages", [])

        # Convert messages to text-only for Groq (Groq doesn't support PDF)
        # Extract text parts only
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
                        # Decode base64 PDF to text hint
                        text_parts.append("[Resume PDF uploaded by candidate]")
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

        # Normalize to Claude-like format for frontend compatibility
        return jsonify({
            "content": [{"type": "text", "text": text}]
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
