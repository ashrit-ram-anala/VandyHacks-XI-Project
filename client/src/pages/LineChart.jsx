import { useState, useEffect } from "react";
import { Line } from "react-chartjs-2";
import Chart from "chart.js/auto";
import axios from 'axios'
import { CategoryScale } from "chart.js";



function LineChart() {
  Chart.register(CategoryScale);
  const [chartData,setCharData] = useState({
    labels: ["2016", "2017", "2018", "2019", "2020"],
    datasets: [
      {
        label: "Users Gained",
        data: [],
        fill: false,
        borderColor: "rgba(75,192,192,1)",
        backgroundColor: "rgba(0,0,0,0.1)",
      },
    ],
  });

let fetched=[10,20,70]

  useEffect(()=>{
    axios.get("http://localhost:8080/api/sentiment/:AAPL")
    .then((response)=>{
     fetched = response.data
     console.log(fetched)
    })
    setCharData({
      labels: [],
      datasets: [
        {
          label: "Sentiment",
          data: fetched,
          fill: false,
          borderColor: "rgba(75,192,192,1)",
          backgroundColor: "rgba(0,0,0,0.1)",
        },
      ],
    });
  },[])



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
