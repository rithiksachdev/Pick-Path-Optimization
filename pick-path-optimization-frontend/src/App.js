import logo from './logo.svg';
import './App.css';
import RangeSliderWave from './WaveSimulationSlider';
import { BrowserRouter, Routes, Route } from "react-router-dom";
import RangeSliderBatch from './BatchSimulationSlider';
import RouteSimulation from './Route';
import Results from './result';
import Landing from './landing';
import ResultsCluster from './result2';
import ResultsRoute from './result3';
import StoreLayout from './storeLayout';
function App() {
  return (
   <Routes>
<Route exact path="/"> <Landing /> </Route>
  <Route path="/batch"> <RangeSliderBatch /> </Route>
  <Route path="/wave"> <RangeSliderWave /> </Route>
  <Route path="/route"> <RouteSimulation /> </Route>
  <Route path="/result"> <Results /> </Route>
  <Route path="/resultCluster"> <ResultsCluster /> </Route>
  <Route path="/layout"> < StoreLayout/> </Route>
  <Route path="/resultRoute"> <ResultsRoute /> </Route>
</Routes>
  );
    
    {/* // <div className="App">
    //  <RangeSliderWave/>
    // </div>); */}
  
}

export default App;
