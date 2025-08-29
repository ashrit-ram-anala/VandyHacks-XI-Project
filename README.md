# Smart-Stock

Smart-Stock is a web application made for **VandyHacks XI** that allows users to enter specific stock tickers (AAPL, AMZN, etc.) and see the public sentiment for those stocks at that very moment. The sentiments are tracked and displayed in real time with Chart.js. Smart-Stock utilizes the Reddit API and performs **Sentiment Analysis** with Python **TextBlob**

# Overview

## Frontend

#### React.JS + Vite, Chart.JS, Tailwind CSS, DaisyUI

## Backend

#### Flask, TextBlob (Sentiment Analysis)

# Installation

**Clone The Github Repository:**

```
git clone <SSH/HTTPS Key>
```

**Install Frontend Dependencies:**

```
cd client
npm i
```

**Install Backend Dependencies:**

```
cd ../server
npm i
```

**Go to package.json and add the following scripts:**

```
"start": "node server"
"dev": "nodemon server"
```

**Run Frontend App With:**

```
npm run dev
```
in client folder

**Run Backend App With:**
```
python3 app.py
```
in server folder

# Preview
<img width="1440" height="775" alt="Screenshot 2025-08-29 at 1 09 09 AM" src="https://github.com/user-attachments/assets/965ab081-d7f4-4e45-905f-754ab443d7f4" />
