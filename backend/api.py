from flask import Flask, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

# -------------------------------
# GITHUB RAW JSON URL
# -------------------------------
PROCESSED_NEWS_URL = (
    "https://raw.githubusercontent.com/"
    "vasu-watts/AI-based-Aggregator-Data/main/data/processed_news.json"
)

@app.route("/healthz", methods=["GET"])
def healthz():
    return "OK", 200

@app.route("/news", methods=["GET"])
def get_news():
    try:
        r = requests.get(PROCESSED_NEWS_URL, timeout=10)
        r.raise_for_status()
        return jsonify(r.json()), 200
    except Exception as e:
        return jsonify({
            "error": "Failed to fetch news",
            "details": str(e)
        }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

