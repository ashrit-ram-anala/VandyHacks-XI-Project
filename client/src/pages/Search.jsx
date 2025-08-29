

import React, { useState } from "react";
import axios from "axios";
import "tailwindcss/tailwind.css";
import SentimentChart from "./SentimentChart";

function Search() {
    const [searchQuery, setSearchQuery] = useState("");
    const [sentiment, setSentiment] = useState(null);
    const [posts, setPosts] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    const handleChange = (event) => {
        setSearchQuery(event.target.value);
    };

    const handleSubmit = async (event) => {
        event.preventDefault();
        setLoading(true);
        setError("");
        setSentiment(null);
        setPosts([]);
        try {
            const response = await axios.post("http://127.0.0.1:5000/submit", {
                text: searchQuery,
            });
            setSentiment(response.data);
            if (response.data.posts) {
                if (response.data.post_sentiments) {
                    setPosts(response.data.posts.map((post, idx) => ({ ...post, sentiment: response.data.post_sentiments[idx] })).slice(0, 6));
                } else if (response.data.overall) {
                    setPosts(response.data.posts.map((post) => ({ ...post, sentiment: response.data.overall })).slice(0, 6));
                } else {
                    setPosts(response.data.posts.slice(0, 6));
                }
            }
        } catch (err) {
            setError("Error fetching sentiment. Please try again.");
        }
        setLoading(false);
    };

    return (
        <div className="min-h-screen bg-base-200 flex flex-col items-center p-4">
            <div className="w-full flex flex-col items-center" style={{ marginTop: "40px" }}>
                <h2 className="text-4xl font-bold mb-6 text-center">Smart-Stock Sentiment Search</h2>
                <form onSubmit={handleSubmit} className="flex flex-col gap-4 w-full" style={{ maxWidth: "500px" }}>
                    <input
                        type="text"
                        className="input input-bordered w-full"
                        placeholder="Enter Stock Ticker (e.g. AAPL, AMZN)"
                        value={searchQuery}
                        onChange={handleChange}
                        required
                    />
                    <button type="submit" className="btn btn-primary w-full" disabled={loading}>
                        {loading ? "Searching..." : "Search"}
                    </button>
                </form>
                {error && <div className="alert alert-error mt-4">{error}</div>}
            </div>
            <div className="card w-full" style={{ maxWidth: "80vw", marginTop: "16px" }}>
                <div className="card-body">
                {posts.length > 0 && (
                    <div className="mt-4">
                        <h3 className="text-xl font-semibold mb-2 text-center">Reddit Sentiment</h3>
                        <div className="grid grid-cols-3 gap-4" style={{ width: "100%" }}>
                            {posts.map((post, idx) => (
                                <div key={idx} className="bg-base-300 rounded-lg p-4 text-sm flex flex-col justify-between" style={{ maxHeight: "120px", overflow: "hidden" }}>
                                    <strong>{post.title}</strong>
                                    <div>
                                        {post.body.length > 120 ? post.body.slice(0, 120) + "..." : post.body}
                                    </div>
                                    <div className="mt-2 text-center" style={{ minHeight: "28px" }}>
                                        <span className={`badge badge-sm ${post.sentiment === 'Bullish' ? 'badge-success' : post.sentiment === 'Bearish' ? 'badge-error' : post.sentiment === 'Neutral' ? 'badge-warning' : 'badge-secondary'}`}>{post.sentiment ? post.sentiment : "N/A"}</span>
                                    </div>
                                </div>
                            ))}
                        </div>
                        {sentiment?.sentiment_values && (
                            <SentimentChart sentimentValues={sentiment.sentiment_values} />
                        )}
                        <div className="mt-6 text-center">
                            <span className="badge badge-lg badge-info">
                                Overall Sentiment: {sentiment?.overall || "N/A"}
                            </span>
                        </div>
                    </div>
                )}
                </div>
            </div>
        </div>
    );
}

export default Search;