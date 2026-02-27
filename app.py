from flask import Flask, render_template, request, jsonify
from google import genai
import os

# =========================
# LOAD ENV VARIABLE (Correct Way)
# =========================
API_KEY = os.environ.get("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY is not set in environment variables")

# =========================
# FLASK APP
# =========================
app = Flask(__name__)

# =========================
# GEMINI CLIENT
# =========================
client = genai.Client(api_key=API_KEY)
MODEL_NAME = "gemini-2.5-flash-lite"

# =========================
# ROUTES
# =========================
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json or {}
    user_msg = data.get("message", "").strip()

    if not user_msg:
        return jsonify({"reply": "⚠️ Empty message received"})

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=user_msg
        )

        if not response or not response.text:
            return jsonify({"reply": "⚠️ Model returned no response."})

        return jsonify({"reply": response.text.strip()})

    except Exception as e:
        print("MODEL ERROR:", e)
        return jsonify({"reply": "⚠️ Internal model error."})

# =========================
# RENDER PORT CONFIG
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)