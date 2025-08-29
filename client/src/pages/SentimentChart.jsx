import React from "react";
import { Line } from "react-chartjs-2";
import Chart from "chart.js/auto";

function SentimentChart({ sentimentValues }) {
  if (!sentimentValues || sentimentValues.length === 0) return null;

  const chartData = {
    labels: sentimentValues.map((_, idx) => `Post ${idx + 1}`),
    datasets: [
      {
        label: "Reddit Post Sentiment (Polarity)",
        data: sentimentValues,
        fill: false,
        borderColor: "rgba(75,192,192,1)",
        backgroundColor: "rgba(0,0,0,0.1)",
        tension: 0.2,
      },
      {
        label: "Neutral Opinion (0)",
        data: Array(sentimentValues.length).fill(0),
        borderColor: "#ef4444",
        borderDash: [6, 6],
        pointRadius: 0,
        fill: false,
        backgroundColor: "rgba(0,0,0,0)",
        tension: 0,
      },
    ],
  };

  return (
    <div style={{ width: "100%", maxWidth: "1200px", margin: "32px auto", minHeight: "500px", height: "500px", maxHeight: "500px", overflow: "hidden", display: "flex", justifyContent: "center", alignItems: "center" }}>
      <div style={{ width: "100%", height: "100%" }}>
        <Line
          data={chartData}
          options={{
            plugins: {
              title: {
                display: true,
                text: "Sentiment Polarity of Reddit Posts",
              },
              legend: {
                display: true,
              },
              annotation: {
                annotations: {
                  neutralLine: {
                    type: 'line',
                    yMin: 0,
                    yMax: 0,
                    borderColor: '#ef4444',
                    borderWidth: 2,
                    borderDash: [6, 6],
                    label: {
                      display: true,
                      content: 'Neutral Opinion',
                      position: 'end',
                      color: '#ef4444',
                    },
                  },
                },
              },
            },
            scales: {
              y: {
                min: -1,
                max: 1,
                stepSize: 0.2,
                grid: {
                  display: true,
                  color: "#e5e7eb",
                },
                ticks: {
                  callback: function(value) {
                    return value.toFixed(1);
                  },
                  stepSize: 0.2,
                  font: {
                    size: 14,
                  },
                },
                title: {
                  display: true,
                  text: "Polarity (-1 to 1)",
                  font: {
                    size: 16,
                    weight: "bold",
                  },
                },
              },
              x: {
                grid: {
                  display: false,
                },
                title: {
                  display: true,
                  text: "Reddit Post Index",
                  font: {
                    size: 14,
                  },
                },
              },
            },
            maintainAspectRatio: true,
            responsive: true,
          }}
        />
        <div style={{ textAlign: "center", marginTop: "8px", fontWeight: "bold", color: "#ef4444" }}>
        </div>
      </div>
    </div>
  );
}

export default SentimentChart;
