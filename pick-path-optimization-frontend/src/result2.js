import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import Typography from "@material-ui/core/Typography";
import Slider from "@material-ui/core/Slider";
import axios from "axios";
import SendIcon from '@mui/icons-material/Send'
import "./Slider.css"
import ButtonAppBar from './navbar';
import { TextField,Grid, Button, Icon, Paper } from "@material-ui/core";
import  { useLocation } from 'react-router-dom';
import {
    LineChart,
    ResponsiveContainer,
    Legend, Tooltip,
    Line,
    XAxis,
    YAxis,
    CartesianGrid
} from 'recharts';
  
import img1  from './clustering.png'
import img2  from './cluster_centroids.png'

export default function ResultsCluster() {
  
//   const handleChange = (event, newValue) => {
//     timeout && clearTimeout(timeout);
//     timeout = setTimeout(() => {
//       setValue(newValue); 
//       setOrderLines(newValue);
      
//     }, 1);
//   };
//   const handleVariableChange = (event) => {
//     setN1(event.target.value);
//     //console.log(n1)
//   };


// Sample chart data
const {state} = useLocation();

const pdata = [];

console.log(state)
for (const [key, value] of Object.entries(state.distance_method_1)) {
    console.log(key)
    pdata.push({wave: (Number(key)), distance: value})
}

for (const [key, value] of Object.entries(state.distance_method_2)) {
    console.log(key)
    pdata.push({wave: (Number(key)), distance2: value})
}

for (const [key, value] of Object.entries(state.distance_method_3)) {
    console.log(key)
    pdata.push({wave: (Number(key)), distance3: value})
}

  return (<> <ButtonAppBar/>
  <div class="box offset-bottom-right-shadow"> 
  <h1 className="text-heading">
                Results Chart
            </h1>
            <ResponsiveContainer width="100%" aspect={3}>
                <LineChart data={pdata} margin={{ left: 250 }}>
                    <CartesianGrid />
                    <XAxis dataKey="wave" name="waves"
                        interval={'preserveStartEnd'} />
                    <YAxis></YAxis>
                    <Legend />
                    <Tooltip />
                    <Line dataKey="distance" name="Distance without clustering algorithm"
                        stroke="black" activeDot={{ r: 8 }} />
                    <Line dataKey="distance2"
                        stroke="red" activeDot={{ r: 8 }} name="Distance with clustering algorithm on single line orders" />
                    <Line dataKey="distance3"
                        stroke="green" activeDot={{ r: 8 }} name="Distance with clustering algorithm on single line and multi line orders" />
                </LineChart>
            </ResponsiveContainer>
            <img name="image" style={{ alignContent: 'center', marginLeft: '100px'}} src = {img1}/>
            <img name="image" style={{ alignContent: 'center', marginLeft: '100px'}} src = {img2}/>
  </div>
</>
  );
}
