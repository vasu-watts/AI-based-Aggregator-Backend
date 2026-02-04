from flask import Flask, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

# -------------------------------
# SIMPLE + SAFE PATH
# -------------------------------
PROCESSED_PATH = "data/processed_news.json"

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
        return jsonify({
            "error": "Processed news not found",
            "path": PROCESSED_PATH
        }), 404

    with open(PROCESSED_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    return jsonify(data), 200

# -------------------------------
# RUN SERVER
# -------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
