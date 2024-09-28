const express = require("express");
const app = express();
const axios = require("axios");
const cors = require("cors");
const mongoose = require('mongoose');
const corsOptions = {origin: ["http://localhost:5173"]};
const PORT = '8080';

app.use(express.json())
app.use(cors(corsOptions));

mongoose.connect('mongodb+srv://ashritramanala:X2f1pLPy48ZFal1s@vandyhackscluster.h7isr.mongodb.net/?retryWrites=true&w=majority&appName=VandyHacksCluster');

const userSchema = new mongoose.Schema({
    tkr: String,
    sentiment: {
        type: [Number],
        default: []
    },
    latestSentiment: Number
})

const userModel = mongoose.model("sentiment", userSchema)

app.post('/api/save-tkr', (req, res) => {
    const { tkr, sentiment, latestSentiment } = req.body;
    userModel.findOne({ tkr })
        .then((existingTkr) => {
            if (existingTkr) {
                    existingTkr.sentiment.push(latestSentiment);
                    existingTkr.latestSentiment = latestSentiment;
                    existingTkr.save()
            } else {
                const newTkr = new userModel({
                    tkr,
                    sentiment: [latestSentiment],
                    latestSentiment: latestSentiment
                });

                newTkr.save()
            }
        })
});


app.get('/api/sentiment/:tkr', (req, res) => {
    const { tkr } = req.params;
    userModel.findOne({ tkr })
        .then((existingTkr) => {
            if (existingTkr) {
                res.json({ sentiment: existingTkr.sentiment });
            } else {                
                res.status(404).json({ message: 'Ticker not found' });
            }
        })
});

app.listen(PORT, ()=>{
    console.log("HELLO");
});