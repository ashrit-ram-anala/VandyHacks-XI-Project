# Smart-Stock

Smart-Stock is a web application made for **VandyHacks XI** that allows users to enter specific stock tickers (AAPL, AMZN, etc.) and see the public sentiment for those stocks at that very moment as well as historical sentiment. The sentiments are tracked and displayed in real time with chart.js. Smart-Stock utilizes the Reddit API and performs **sentiment analysis** with the **Perplexity LLM** and Python **TextBlob**

# Overview

## Frontend

#### React.JS + Vite, Chart.JS, Tailwind CSS, DaisyUI

## Backend

#### Node.JS + Express.JS, Flask (Sentiment Analysis), MongoDB

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

**Run App With:**

```
npm run dev
```

**on both client and server directories**