import { useState } from "react";
import "./index.css";
import Search from "./pages/Search";
import Chart from "chart.js/auto";
import { CategoryScale } from "chart.js";
import "./index.css";
Chart.register(CategoryScale);
function App() {

  return (
    <>
      <Search />
    </>
  );
}

export default App
