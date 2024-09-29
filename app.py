from flask import Flask,request
from flask_cors import CORS
import sqlalchemy as sa 
from sqlalchemy.orm import DeclarativeBase 
from openai import OpenAI
import requests
import time
import json
import threading
import re
import praw
import threading
import yfinance as yf
import requests
import mongoengine as mongoose
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

app = Flask(__name__)
CORS(app) 

@app.route('/')
def index():
    return "Flask server is running!"
@app.route('/api/save-tkr')
def send_json():
    return getComments(reddit.subreddit("all"), company_name)
@app.route('/add_todo', methods=['POST'])
def add_todo():
    todo_data = request.get_json()
    new_todo = Todo(content=todo_data['content'])
    sa.session.add(new_todo)
    sa.session.commit()
    return 'Done', 201
class Todo(DeclarativeBase):
    id = sa.Column(sa.Integer, primary_key=True)
    type = sa.Column(sa.String)
def remove_emoji(text):
    #removes regular emojis
    RE_EMOJI = re.compile(u'([\U00002600-\U000027BF])|([\U0001f300-\U0001f64F])|([\U0001f680-\U0001f6FF])')
    text = RE_EMOJI.sub(r'', text)
    #returns the emojis of the format [emoji](img|string1|string2)
    return re.sub(r'\[.*?\)', '', text)

@app.route('/submit', methods=['POST'])
def submit():
    ticker = request.json
    return json.dumps({"message": "Data received", "data": ticker})
class ExampleSchema(mongoose.Document):
    ticker = mongoose.StringField(required=True)
    sentiments = mongoose.ListField(mongoose.IntField(), required=True)
    latest_sentiment = mongoose.StringField(required=True)

    meta = {
        'collection': 'sentiment'  # Name of the collection in MongoDB
    }

def getComments(subreddit, text) -> None:  
    client = OpenAI(api_key=YOUR_API_KEY, base_url="https://api.perplexity.ai") 
    messages = [
        {
            "role": "system",
            "content": (
                "You are an expert in marketing and assessing the sentiment of reviews. I am going to give you reviews to respond with only 'positive', 'negative', or 'neutral' towards the use of " + text + ". If you cannot create content about the review, rate it as neutral"
            ),
        },
        {
            "role": "user",
            "content": (
                ""
            ),
        },
    ]
    
    for comment in subreddit.stream.comments():
        if text in comment.body.lower():
            comment.body = remove_emoji(comment.body)
            messages[1]["content"] = comment.body
            response = client.chat.completions.create(
                model="llama-3.1-8b-instruct",
                messages=messages,
            )
            analysis = response.choices[0].message.content
            print(analysis)
            if not (analysis == 'Neutral' or analysis == 'Positive' or analysis == 'Negative'):
                continue
            try:
                number = 0 if analysis == 'Neutral' else 1 if analysis == 'Positive' else -1
                sentiments.append(number)
                # producer.send("redditcomments", value=comment_json)
                comment_json = {
                    "tkr": ticker,
                    "sentiment": sentiments,
                    "latestSentiment": analysis
                }
                collection_name.insert_one(comment_json)
                print(number)
                # Save the document to the database
            except Exception as e:
                print("An error occurred:", str(e))
                return json

# Run the Flask app and start the POST request loop in a separate thread
if __name__ == "__main__":
    reddit = praw.Reddit(
        client_id="_lXa7uHKe5fOpKVnOQlktA",
        client_secret="OsWBMbhI5QO6fQdBw-WsGYnwDiHeiw",
        password="DJAJASFINANCIALSERVICES",
        user_agent="testscript by u/fakebot3",
        username="Sad_Warning869",
        ratelimit_seconds=.75)
    sentiments = []
    YOUR_API_KEY = "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"
    ticker = "AMZN"
    valid_ticker=True
    
    #accept input from react
    company = yf.Ticker(ticker)
    uri =   "mongodb+srv://ashritramanala:X2f1pLPy48ZFal1s@vandyhackscluster.h7isr.mongodb.net/?retryWrites=true&w=majority&appName=VandyHacksCluster"
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client['test']
    collection_name = db['sentiments']
           # Save the document to the database
    # example_document.save()
    print("Document Saved")
    try:
        company_name = company.info['longName'].split(" ")[0].split(".")[0].lower()
        getComments(subreddit=reddit.subreddit("all"),text=company_name)
    except:
        valid_ticker=False
        print("Ticker does not exist")
    # Start the POST request function in a background thread
    # post_request_thread = threading.Thread(target=send_json_to_nodejs)
    # post_request_thread.daemon = True  # Ensure thread exits when Flask app stops
    # post_request_thread.start()
    # mongoose.connect("mongodb+srv://ashritramanala:X2f1pLPy48ZFal1s@vandyhackscluster.h7isr.mon godb.net/?retryWrites=true&w=majority&appName=VandyHacksCluster")
 
    # Start the Flask app
    app.run(debug=True)

