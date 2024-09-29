import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import App from "./App.jsx";
import "./index.css";
import LineChart from "./pages/LineChart.jsx";
import { createBrowserRouter, RouterProvider } from "react-router-dom";

const router = createBrowserRouter([
  { path: "/", element: <App /> },
  { path: "/linechart", element: <LineChart /> },
]);

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <>
      <h1>main.jsx</h1>
      <RouterProvider router={router} />
    </>
  </StrictMode>
);
