from flask import Flask, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

# -------------------------------
# ABSOLUTE PATH SETUP (CRITICAL)
# -------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROCESSED_PATH = os.path.join(BASE_DIR, "..", "data", "processed_news.json")

# -------------------------------
# HEALTH CHECK
# -------------------------------
@app.route("/healthz", methods=["GET"])
def healthz():
    return "OK", 200

# -------------------------------
# NEWS API
# -------------------------------
@app.route("/news", methods=["GET"])
def get_news():
    if not os.path.exists(PROCESSED_PATH):
        return jsonify({"error": "Processed news not found"}), 404

    with open(PROCESSED_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    return jsonify(data)

# -------------------------------
# RUN SERVER
# -------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
