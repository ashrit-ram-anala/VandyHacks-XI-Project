from flask import Flask, request
from flask_cors import CORS
import json
import re
import praw
from textblob import TextBlob
from dotenv import load_dotenv
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
load_dotenv()

def remove_emoji(text):
    RE_EMOJI = re.compile(u'([\U00002600-\U000027BF])|([\U0001f300-\U0001f64F])|([\U0001f680-\U0001f6FF])')
    text = RE_EMOJI.sub(r'', text)
    return re.sub(r'\[.*?\)', '', text)

@app.route('/')
def index():
    return "Flask server is running!"


@app.route('/submit', methods=['POST'])
def submit():
    try:
        search_term = request.json.get('text', '').lower()
        posts = reddit.subreddit("stocks").search(search_term, limit=30)
        pos, neg, neu = 0, 0, 0
        post_list = []
        post_sentiments = []
        sentiment_values = []
        for post in posts:
            title = getattr(post, 'title', '')
            body = getattr(post, 'selftext', '')
            text = f"{title} {body}"
            analysis = TextBlob(text)
            polarity = analysis.sentiment.polarity
            sentiment_values.append(polarity)
            if polarity > 0.1:
                sentiment = "Bullish"
                pos += 1
            elif polarity < -0.1:
                sentiment = "Bearish"
                neg += 1
            else:
                sentiment = "Neutral"
                neu += 1
            post_list.append({"title": title, "body": body})
            post_sentiments.append(sentiment)
        if pos > neg:
            overall = "Bullish"
        elif neg > pos:
            overall = "Bearish"
        else:
            overall = "Neutral"
        return json.dumps({
            "posts": post_list,
            "overall": overall,
            "post_sentiments": post_sentiments,
            "sentiment_values": sentiment_values
        })
    except Exception as e:
        print(f"Reddit/TextBlob error: {e}")
        return json.dumps({"error": f"Reddit/TextBlob error: {str(e)}"}), 500

if __name__ == "__main__":
    CLIENT_ID = os.getenv("CLIENT_ID")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET")
    PASSWORD = os.getenv("PASSWORD")
    USER_AGENT = os.getenv("USER_AGENT")
    USERNAME = os.getenv("USERNAME")
    reddit = praw.Reddit(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        password=PASSWORD,
        user_agent=USER_AGENT,
        username=USERNAME,
        ratelimit_seconds=.75)
    app.run(debug=True)