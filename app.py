from flask import Flask, render_template, request, jsonify
from google import genai
import os

# =========================
# 🔐 DIRECT API KEY (SIMPLE)
# =========================
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

    # ⭐ Try preview model first
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
        print("Preview error:", e)

    # ⭐ Fallback model
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_msg
        )
        return jsonify({
            "reply": response.text.strip(),
            "model": "gemini-2.5-flash"
        })

    except Exception as e:
        print("Fallback error:", e)

    return jsonify({
        "reply": "AI service temporarily unavailable."
    })


# =========================
# ▶️ RENDER PORT SETTINGS
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
