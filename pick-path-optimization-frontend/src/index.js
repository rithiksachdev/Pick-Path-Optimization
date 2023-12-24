// import React from 'react';
// import ReactDOM from 'react-dom/client';
// import './index.css';
// import App from './App';
// import reportWebVitals from './reportWebVitals';

// const root = ReactDOM.createRoot(document.getElementById('root'));
// root.render(
//   <React.StrictMode>
//     <App />
//   </React.StrictMode>
// );

// // If you want to start measuring performance in your app, pass a function
// // to log results (for example: reportWebVitals(console.log))
// // or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
// reportWebVitals();

import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Landing from "./landing";
import RangeSliderBatch from "./BatchSimulationSlider";
import RangeSliderWave from "./WaveSimulationSlider";
import RouteSimulation from "./Route";
import Results from "./result";
import ResultsCluster from "./result2";
import ResultsRoute from "./result3";
import StoreLayout from "./storeLayout";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>       
          {/* <Route index element={<Landing />} /> */}
          <Route path="wave" element={<RangeSliderWave />} />
          <Route path="batch" element={<RangeSliderBatch />} />
          <Route path="route" element={<RouteSimulation />} />
          <Route path="result" element={<Results />} />
          <Route path="resultCluster" element={<ResultsCluster />} />
          <Route path="storeLayout" element={<StoreLayout />} />
          <Route path="resultRoute" element={<ResultsRoute />} />
          <Route exact path="/" element={<Landing />}>
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);
