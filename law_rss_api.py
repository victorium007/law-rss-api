from flask import Flask, jsonify, request
import feedparser

app = Flask(__name__)

# מיפוי של מילות מפתח לכתובות RSS באתר law.co.il
RSS_FEEDS = {
    "פרטיות": "https://www.law.co.il/rss/privacy.xml",
    "קניין רוחני": "https://www.law.co.il/rss/intellectual-property.xml",
    "סייבר": "https://www.law.co.il/rss/privacy.xml",
    "זכויות יוצרים": "https://www.law.co.il/rss/copyright.xml",
    "פטנטים": "https://www.law.co.il/rss/patents.xml",
    "תוכנה": "https://www.law.co.il/rss/software.xml",
    "מסחר אלקטרוני": "https://www.law.co.il/rss/ecommerce.xml",
    "דיני עבודה": "https://www.law.co.il/rss/labor-law.xml",
    "הגנת צרכן": "https://www.law.co.il/rss/consumer.xml"
}

@app.route("/")
def home():
    return "Law.co.il RSS API is running"

@app.route("/list-topics")
def list_topics():
    return jsonify(list(RSS_FEEDS.keys()))

@app.route("/search-feed")
def search_feed():
    query = request.args.get("q", "")
    best_match = next((k for k in RSS_FEEDS if query in k), None)
    if best_match:
        return jsonify({"topic": best_match, "feed_url": RSS_FEEDS[best_match]})
    return jsonify({"error": "לא נמצא פיד מתאים"}), 404

@app.route("/latest", methods=["GET"])
def latest_cases():
    topic = request.args.get("topic")
    count = int(request.args.get("count", 5))

    if topic not in RSS_FEEDS:
        return jsonify({"error": "נושא לא נתמך"}), 400

    feed_url = RSS_FEEDS[topic]
    feed = feedparser.parse(feed_url)

    results = []
    for entry in feed.entries[:count]:
        results.append({
            "title": entry.title,
            "summary": entry.summary,
            "link": entry.link,
            "published": entry.published
        })

    return jsonify(results)

if __name__ == "__main__":
    app.run(port=5000)
