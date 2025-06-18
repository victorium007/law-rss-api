from flask import Flask, request, jsonify
from flask_cors import CORS
import feedparser
import os

app = Flask(__name__)
CORS(app)

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

    response = jsonify(results[:5])
    response.headers['Content-Type'] = 'application/json'
    return response
    
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))  # השג פורט מ-Render
    app.run(host="0.0.0.0", port=port)        # האזן לכל הכתובות בפורט הזה
