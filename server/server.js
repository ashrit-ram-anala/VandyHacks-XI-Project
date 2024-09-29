const express = require("express");
const mongoose = require("mongoose");
const cors = require("cors");
const axios = require("axios");

const app = express();
const corsOptions = { origin: ["http://localhost:5173", "http://localhost:5000"] };
const PORT = "8080";

app.use(express.json());
app.use(cors(corsOptions));

mongoose.connect(
  "mongodb+srv://ashritramanala:X2f1pLPy48ZFal1s@vandyhackscluster.h7isr.mongodb.net/?retryWrites=true&w=majority&appName=VandyHacksCluster"
);

const userSchema = new mongoose.Schema({
  tkr: String,
  sentiment: {
    type: [Number],
    default: [],
  },
  latestSentiment: Number,
});

const userModel = mongoose.model("sentiment", userSchema);

app.post("/api/save-tkr", (req, res) => {
  const { tkr, sentiment, latestSentiment } = req.body; // cound remove sentiment
  const existingTkr = userModel.findOne({ tkr });
  // .then((existingTkr) => {
  if (existingTkr) {
    // if tker already logged
    existingTkr.sentiment.push(latestSentiment);
    existingTkr.latestSentiment = latestSentiment;
    existingTkr.save();
  } else {
    // if tker not already logged
    const newTkr = new userModel({
      tkr,
      sentiment: [latestSentiment],
      latestSentiment: latestSentiment,
    });

    newTkr.save();
  }
  // })
});

app.get("/api/sentiment/:tkr", (req, res) => {
  const { tkr } = req.params;
  userModel.findOne({ tkr })
  .then((existingTkr) => {
  if (existingTkr) {
    res.json({ sentiment: existingTkr.sentiment });
  } else {
    res.status(404).json({ message: "Ticker not found" });
  }
   })
});

app.listen(PORT, () => {
  console.log("HELLO");
});
