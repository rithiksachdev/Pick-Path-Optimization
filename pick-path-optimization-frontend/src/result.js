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



export default function Results() {
  
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
console.log(state.distance)
for (const [key, value] of Object.entries(state.distance)) {
    console.log(key)
    pdata.push({wave: (Number(key) + 1), distance: value})
}

  return (<> <ButtonAppBar/>
  <div class="box offset-bottom-right-shadow"> 
  <h1 className="text-heading">
                Results Chart
            </h1>
            <ResponsiveContainer width="100%" aspect={3}>
                <LineChart data={pdata} margin={{ left: 250 }}>
                    <CartesianGrid />
                    <XAxis dataKey="wave" 
                        interval={'preserveStartEnd'} />
                    <YAxis></YAxis>
                    <Legend />
                    <Tooltip />
                    <Line dataKey="distance" name="Y - Distance"
                        stroke="black" activeDot={{ r: 8 }} />
                                        <Line dataKey="X - waves"
                        stroke="red" activeDot={{ r: 8 }} />
                </LineChart>
            </ResponsiveContainer>
  </div>
</>
  );
}
