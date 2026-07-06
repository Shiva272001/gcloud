from flask import Flask, request, jsonify
from app import ask_citymind
import os

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "online",
        "project": "CityMind AI Platform",
        "message": "Welcome! The backend API is running successfully. Send POST requests to /ask to interact with the agent."
    }), 200

@app.route("/ask", methods=["POST"])
def ask():
    question = request.json.get("question", "")
    answer = ask_citymind(question)
    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))