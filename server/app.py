from flask import Flask, request
from flask_cors import CORS
import json
import re
import praw
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
from dotenv import load_dotenv
import os
import numpy as np

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
load_dotenv()

STOCK_SENTIMENT_LEXICON = {
    'moon': (0.9, 0.8),
    'rocket': (0.85, 0.8),
    'bullish': (0.8, 0.7),
    'surge': (0.75, 0.6),
    'rally': (0.7, 0.6),
    'breakout': (0.7, 0.6),
    'gainz': (0.8, 0.7),
    'gains': (0.7, 0.6),
    'mooning': (0.9, 0.8),
    'tendie': (0.8, 0.7),
    'tendies': (0.8, 0.7),
    'calls': (0.6, 0.5),
    'long': (0.5, 0.5),
    'buy': (0.6, 0.6),
    'buying': (0.6, 0.6),
    'hodl': (0.7, 0.7),
    'hold': (0.5, 0.5),
    'diamond hands': (0.8, 0.8),
    'upgrade': (0.7, 0.6),
    'beat': (0.6, 0.5),
    'outperform': (0.7, 0.6),
    'strong buy': (0.9, 0.7),
    'conviction': (0.6, 0.5),
    'bullish af': (0.95, 0.9),
    'crash': (-0.85, 0.7),
    'dump': (-0.8, 0.7),
    'bearish': (-0.8, 0.7),
    'tank': (-0.75, 0.6),
    'plummet': (-0.8, 0.7),
    'collapse': (-0.85, 0.7),
    'puts': (-0.6, 0.5),
    'short': (-0.6, 0.6),
    'shorting': (-0.6, 0.6),
    'sell': (-0.6, 0.6),
    'selling': (-0.6, 0.6),
    'paper hands': (-0.7, 0.7),
    'bagholding': (-0.6, 0.6),
    'bagholder': (-0.6, 0.6),
    'rekt': (-0.85, 0.8),
    'downgrade': (-0.7, 0.6),
    'miss': (-0.6, 0.5),
    'underperform': (-0.7, 0.6),
    'overvalued': (-0.6, 0.5),
    'bubble': (-0.7, 0.6),
    'correction': (-0.5, 0.5),
    'dip': (-0.4, 0.4),
    'loss': (-0.7, 0.6),
    'losses': (-0.7, 0.6),
    'volatility': (0.0, 0.8),
    'volatile': (0.0, 0.7),
    'speculation': (0.0, 0.8),
    'earnings': (0.0, 0.3),
    'ipo': (0.0, 0.4),
}

def remove_emoji(text):
    RE_EMOJI = re.compile(u'([\U00002600-\U000027BF])|([\U0001f300-\U0001f64F])|([\U0001f680-\U0001f6FF])')
    text = RE_EMOJI.sub(r'', text)
    return re.sub(r'\[.*?\)', '', text)

def apply_custom_lexicon(text, base_polarity):
    text_lower = text.lower()
    custom_score = 0
    word_count = 0

    for phrase, (polarity, _) in STOCK_SENTIMENT_LEXICON.items():
        if ' ' in phrase and phrase in text_lower:
            custom_score += polarity * 2.0
            word_count += 1

    words = text_lower.split()
    for word in words:
        if word in STOCK_SENTIMENT_LEXICON:
            polarity, _ = STOCK_SENTIMENT_LEXICON[word]
            custom_score += polarity * 1.5
            word_count += 1

    if word_count > 0:
        avg_custom_score = custom_score / word_count
        blended_score = (avg_custom_score * 0.7) + (base_polarity * 0.3)
        return blended_score

    return base_polarity

def enhanced_sentiment_analysis(text):
    blob_pattern = TextBlob(text)
    pattern_polarity = blob_pattern.sentiment.polarity

    try:
        blob_nb = TextBlob(text, analyzer=NaiveBayesAnalyzer())
        nb_classification = blob_nb.sentiment.classification
        nb_p_pos = blob_nb.sentiment.p_pos
        nb_p_neg = blob_nb.sentiment.p_neg
        nb_polarity = (nb_p_pos - nb_p_neg)
    except Exception as e:
        print(f"Naive Bayes analysis failed: {e}")
        nb_polarity = 0
        nb_classification = "neutral"

    custom_polarity = apply_custom_lexicon(text, pattern_polarity)
    final_polarity = (custom_polarity * 0.40) + (nb_polarity * 0.35) + (pattern_polarity * 0.25)

    return {
        'polarity': final_polarity,
        'pattern_polarity': pattern_polarity,
        'nb_polarity': nb_polarity,
        'nb_classification': nb_classification,
        'custom_polarity': custom_polarity
    }

@app.route('/')
def index():
    return "Flask server is running!"


@app.route('/submit', methods=['POST'])
def submit():
    try:
        search_term = request.json.get('text', '').lower()
        posts = reddit.subreddit("stocks").search(search_term, limit=1000)
        pos, neg, neu = 0, 0, 0
        post_list = []
        post_sentiments = []
        sentiment_values = []
        detailed_analysis = []

        for post in posts:
            title = getattr(post, 'title', '')
            body = getattr(post, 'selftext', '')
            text = f"{title} {body}"

            analysis_result = enhanced_sentiment_analysis(text)
            polarity = analysis_result['polarity']

            sentiment_values.append(polarity)

            if polarity > 0.15:
                sentiment = "Bullish"
                pos += 1
            elif polarity < -0.15:
                sentiment = "Bearish"
                neg += 1
            else:
                sentiment = "Neutral"
                neu += 1

            post_list.append({"title": title, "body": body})
            post_sentiments.append(sentiment)

            detailed_analysis.append({
                'title': title[:100],
                'final_polarity': round(polarity, 4),
                'pattern_polarity': round(analysis_result['pattern_polarity'], 4),
                'nb_polarity': round(analysis_result['nb_polarity'], 4),
                'nb_classification': analysis_result['nb_classification'],
                'custom_polarity': round(analysis_result['custom_polarity'], 4),
                'sentiment': sentiment
            })

        avg_polarity = np.mean(sentiment_values) if sentiment_values else 0

        if avg_polarity > 0.1 and pos > neg:
            overall = "Bullish"
        elif avg_polarity < -0.1 and neg > pos:
            overall = "Bearish"
        else:
            overall = "Neutral"

        return json.dumps({
            "posts": post_list,
            "overall": overall,
            "post_sentiments": post_sentiments,
            "sentiment_values": sentiment_values,
            "average_sentiment": float(avg_polarity),
            "sentiment_counts": {
                "bullish": pos,
                "bearish": neg,
                "neutral": neu
            },
            "detailed_analysis": detailed_analysis[:10]
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
