from flask import Flask, render_template, request, jsonify
from google import genai
from dotenv import load_dotenv
import os

# =========================
# LOAD ENV
# =========================
load_dotenv()
API_KEY = "GEMINI_API_KEY"

# =========================
# FLASK APP
# =========================
app = Flask(__name__)

# =========================
# GEMINI CLIENT
# =========================
client = genai.Client(api_key=API_KEY)

# 👉 Change model here easily
MODEL_NAME = "gemini-2.5-flash"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json or {}
    user_msg = data.get("message", "").strip()

    if not user_msg:
        return jsonify({"reply": "Please type a message."})

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=user_msg
    )

    return jsonify({
        "reply": response.text.strip(),
        "model": MODEL_NAME
    })

if __name__ == "__main__":
    print("🚀 Running at http://127.0.0.1:5000")
    app.run(debug=True)