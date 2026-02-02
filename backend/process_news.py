import json
import pandas as pd
from bs4 import BeautifulSoup
from sklearn.cluster import KMeans
from sentence_transformers import SentenceTransformer
from datetime import datetime, timezone
import os

# -------------------------------
# BASE DIRECTORY (CRITICAL FIX)
# -------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

INPUT_FILE = os.path.join(BASE_DIR, "..", "data", "news_raw.json")
OUTPUT_FILE = os.path.join(BASE_DIR, "..", "data", "processed_news.json")

N_CLUSTERS = 6

# -------------------------------
# CLEAN TEXT FUNCTIONS
# -------------------------------
def clean_text(html):
    if not html:
        return ""
    return BeautifulSoup(html, "html.parser").get_text(" ", strip=True)

def load_articles():
    if not os.path.exists(INPUT_FILE):
        print("[ERROR] news_raw.json not found")
        return []

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        return json.load(f).get("articles", [])

def prepare_texts(articles):
    return [
        f"{a.get('title','')} {clean_text(a.get('summary',''))}"
        for a in articles
    ]

# -------------------------------
# MAIN PROCESSING
# -------------------------------
def main():
    print("[INFO] Loading articles...")
    articles = load_articles()

    if not articles:
        print("[ERROR] No articles found, aborting clustering")
        return

    print(f"[INFO] {len(articles)} articles loaded")

    print("[INFO] Preparing text for embeddings...")
    texts = prepare_texts(articles)

    print("[INFO] Generating embeddings...")
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(texts, convert_to_numpy=True)

    print("[INFO] Clustering articles...")
    kmeans = KMeans(
        n_clusters=N_CLUSTERS,
        random_state=42,
        n_init=10
    )
    labels = kmeans.fit_predict(embeddings)

    # -------------------------------
    # CREATE DATAFRAME
    # -------------------------------
    df = pd.DataFrame({
        "title": [a.get("title", "") for a in articles],
        "url": [a.get("link", "") for a in articles],
        "source": [a.get("source", "Unknown") for a in articles],
        "published": [a.get("published", "") for a in articles],
        "region": [a.get("region", "GLOBAL") for a in articles],
        "cluster": labels
    })

    # -------------------------------
    # BUILD CLUSTERS
    # -------------------------------
    clusters = []
    for cluster_id in range(N_CLUSTERS):
        cluster_articles = df[df["cluster"] == cluster_id].to_dict(orient="records")
        clusters.append({
            "group_id": int(cluster_id),
            "articles": cluster_articles
        })

    # -------------------------------
    # FINAL OUTPUT
    # -------------------------------
    output = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "total_articles": len(articles),
        "clusters": clusters
    }

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

    print("[INFO] Saving processed news...")
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print("[SUCCESS] Processed news saved at:", output["generated_at_utc"])

# -------------------------------
# ENTRY POINT
# -------------------------------
if __name__ == "__main__":
    main()
