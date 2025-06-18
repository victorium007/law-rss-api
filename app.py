from flask import Flask, request, jsonify
from flask_cors import CORS
import feedparser
import os
from datetime import datetime, timedelta
import time

app = Flask(__name__)
CORS(app)

@app.route('/search', methods=['GET'])
def search_law_rss():
    keyword = request.args.get('keyword', '').lower()
    feed_url = "https://www.law.co.il/rss/"
    # שימוש ב-agent מותאם כמו RSS Reader
    feed = feedparser.parse(feed_url, agent='Mozilla/5.0 (RSS Reader)')
    results = []

    cutoff_date = datetime.now() - timedelta(days=60)

    for entry in feed.entries:
        if hasattr(entry, 'published_parsed'):
            entry_date = datetime.fromtimestamp(time.mktime(entry.published_parsed))
            if entry_date < cutoff_date:
                continue

        if keyword in entry.title.lower() or keyword in entry.get("description", "").lower():
            results.append({
                "title": entry.title,
                "date": entry.published,
                "link": entry.link
            })

    response = jsonify(results[:10])
    response.headers['Content-Type'] = 'application/json'
    return response

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
