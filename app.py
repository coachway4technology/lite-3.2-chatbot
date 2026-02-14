from flask import Flask, render_template, request, jsonify
from google import genai
from dotenv import load_dotenv
import os

# =========================
# 🔐 LOAD ENV
# =========================
load_dotenv()

API_KEY = "GEMINI_API_KEY"



# =========================
# 🚀 FLASK APP
# =========================
app = Flask(__name__)

# =========================
# 🤖 GENAI CLIENT
# =========================
client = genai.Client(api_key=API_KEY)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json or {}

    user_msg = data.get("message", "").strip()

    if not user_msg:
        return jsonify({"reply": "Please type a message."})

    if len(user_msg) > 2500:
        return jsonify({"reply": "Message too long."})

    # =========================
    # 1️⃣ TRY GEMINI 3 FLASH PREVIEW
    # =========================
    try:
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=user_msg
        )
        return jsonify({
            "reply": response.text.strip(),
            "model": "gemini-3-flash-preview"
        })

    except Exception as e:
        print("⚠️ Preview model busy:", e)

    # =========================
    # 2️⃣ FALLBACK TO STABLE MODEL
    # =========================
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_msg
        )
        return jsonify({
            "reply": response.text.strip(),
            "model": "gemini-2.5-flash (fallback)"
        })

    except Exception as e:
        print("❌ Fallback failed:", e)

    return jsonify({
        "reply": "⚠️ AI service temporarily unavailable. Please try again.",
        "model": "none"
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Render dynamic port
    print(f"🚀 Running on port {port}")
    app.run(host="0.0.0.0", port=port)
