from flask import Flask, request, jsonify
from flask_cors import CORS
import feedparser
import os

app = Flask(__name__)
CORS(app)

@app.route('/debug', methods=['GET'])
def debug_rss_fields():
    feed_url = "https://www.law.co.il/rss/"
    feed = feedparser.parse(feed_url)
    results = []

    for entry in feed.entries:
        results.append({
            "title": entry.get("title", ""),
            "fields": list(entry.keys())
        })

    return jsonify(results)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
