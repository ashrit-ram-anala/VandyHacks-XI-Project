import React from "react";
import { Line } from "react-chartjs-2";

const chartData = {
  labels: ["2016", "2017", "2018", "2019", "2020"],
  datasets: [
    {
      label: "Users Gained",
      data: [500, 100, 400, 200, 300],
      fill: false,
      borderColor: "rgba(75,192,192,1)",
      backgroundColor: "rgba(0,0,0,0.1)",
    },
  ],
};

function LineChart() {
  return (
    <div className="chart-container">
      <h2 style={{ textAlign: "center" }}>Stock Performances</h2>
      <Line
        data={chartData}
        options={{
          plugins: {
            title: {
              display: true,
              text: "User Sentiment over Time",
            },
            legend: {
              display: false,
            },
          },
        }}
        style={{
          backgroundColor: "rgba(255, 255, 255, 1)", // background color
          padding: "20px",
        }}
      />
    </div>
  );
}

export default LineChart;
