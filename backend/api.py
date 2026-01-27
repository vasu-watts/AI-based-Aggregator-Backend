from flask import Flask, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)   # <-- This allows React frontend to fetch data from Flask

PROCESSED_PATH = "../data/processed_news.json"

@app.route("/healthz", methods=["GET"])
def healthz():
    return "OK", 200

@app.route("/news", methods=["GET"])
def get_news():
    if not os.path.exists(PROCESSED_PATH):
        return jsonify({"error": "Processed news not found"}), 404

    with open(PROCESSED_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
