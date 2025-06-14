
from flask import Flask, request, jsonify
import feedparser

app = Flask(__name__)

@app.route('/search', methods=['GET'])
def search_law_rss():
    keyword = request.args.get('keyword', '').lower()
    feed_url = "https://www.law.co.il/rss/"
    feed = feedparser.parse(feed_url)
    results = []

    for entry in feed.entries:
        if keyword in entry.title.lower() or keyword in entry.summary.lower():
            results.append({
                "title": entry.title,
                "date": entry.published,
                "link": entry.link
            })

    return jsonify(results[:5])  # נחזיר עד 5 תוצאות
