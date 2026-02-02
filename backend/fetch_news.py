import feedparser
import json
from datetime import datetime, timezone
import os

# -------------------------------
# BASE DIRECTORY (CRITICAL)
# -------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(BASE_DIR, "..", "data", "news_raw.json")

# -----------------------------------
# REGION-WISE GOOGLE NEWS RSS FEEDS
# -----------------------------------
RSS_FEEDS = {
    "GLOBAL": "https://news.google.com/rss?hl=en&gl=US&ceid=US:en",
    "INDIA": "https://news.google.com/rss?hl=en-IN&gl=IN&ceid=IN:en",
    "US": "https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en",
    "EUROPE": "https://news.google.com/rss?hl=en-GB&gl=GB&ceid=GB:en",
    "ASIA": "https://news.google.com/rss?hl=en-SG&gl=SG&ceid=SG:en"
}

# -------------------------------
# FETCH NEWS
# -------------------------------
def fetch_news():
    all_articles = []
    seen_links = set()

    for region, url in RSS_FEEDS.items():
        print(f"[INFO] Fetching news for region: {region}")
        feed = feedparser.parse(url)

        for entry in feed.entries:
            link = entry.link

            # Deduplicate across regions
            if link in seen_links:
                continue
            seen_links.add(link)

            article = {
                "title": entry.title,
                "link": link,
                "published": entry.published if hasattr(entry, "published") else "",
                "summary": entry.summary if hasattr(entry, "summary") else "",
                "source": entry.source.title if hasattr(entry, "source") else "Google News",
                "region": region
            }

            all_articles.append(article)

    return all_articles

# -------------------------------
# SAVE NEWS
# -------------------------------
def save_news(articles):
    data = {
        "last_updated_utc": datetime.now(timezone.utc).isoformat(),
        "total_articles": len(articles),
        "articles": articles
    }

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# -------------------------------
# ENTRY POINT
# -------------------------------
if __name__ == "__main__":
    news = fetch_news()
    save_news(news)
    print(f"[SUCCESS] Fetched {len(news)} unique articles across all regions.")
