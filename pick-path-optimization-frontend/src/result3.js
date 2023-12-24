import { makeStyles } from "@material-ui/core/styles";
import Typography from "@material-ui/core/Typography";
import Slider from "@material-ui/core/Slider";
import axios, { all } from "axios";
import SendIcon from '@mui/icons-material/Send'
import "./Slider.css"
import "./result3.css"
import ButtonAppBar from './navbar';
import { TextField,Grid, Button, Icon, Paper } from "@material-ui/core";
import  { useLocation } from 'react-router-dom';
import React, { PureComponent } from 'react';
import {
    LineChart,
    ResponsiveContainer,
    Legend, Tooltip,
    Line,
    XAxis,
    YAxis,
    CartesianGrid
} from 'recharts';

import item1 from './item1.jpg'
import item2 from './item2.jpg'
import item3 from './item3.jpg'
import item4 from './item4.jpg'
import img1 from './warehouse_layout.png'

import { type } from "@testing-library/user-event/dist/type";



export default function ResultsRoute() {
  
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
console.log(state.routes)
const routeDict = state.routes
var route = routeDict[Object.keys(routeDict)[Object.keys(routeDict).length - 1]]
console.log(route)
for (const [key, value] of Object.entries(route)) {
    pdata.push({name: 'Here', x: value[0], y: value[1]})
}
console.log(pdata)

// const data = [
//     { x: 1, y: 23 },
//     { x: 2, y: 3 },
//     { x: 3, y: 15 },
//     { x: 4, y: 35 },
//     { x: 5, y: 45 },
//     { x: 6, y: 25 },
//     { x: 7, y: 17 },
//     { x: 8, y: 32 },
//     { x: 9, y: 43 },
// ];

// const data01 = [
//     { x: 10, y: 30 },
//     { x: 30, y: 200 },
//     { x: 45, y: 100 },
//     { x: 50, y: 400 },
//     { x: 70, y: 150 },
//     { x: 100, y: 250 },
//   ];
//   const data02 = [
//     { x: 30, y: 20 },
//     { x: 50, y: 180 },
//     { x: 75, y: 240 },
//     { x: 100, y: 100 },
//     { x: 120, y: 190 },
//   ];


const data = [
    {
      itemId: '01',
      itemName: 'iphone 14 pro',
      SKU: '453963',
      department: 'Mobile department',
      location: 'X: 15.25, Y: 21.0',
      alley: 'A11 20',
      imageHTML: <img name="image" style={{width: '200px', height: '200px', alignContent: 'center', marginLeft: '100px'}} src = {item1}/>,
    },
    {
      itemId: '02',
      itemName: 'Headphones',
      SKU: '442479',
      department: 'Electronics',
      location: 'X: 19.5, Y: 19.5',
      alley: 'A11 17',
      imageHTML: <img name="image" style={{width: '200px', height: '200px', alignContent: 'center', marginLeft: '100px'}} src = {item2}/>,
    },
    {
        itemId: '03',
        itemName: 'Nail polish',
        SKU: '448369',
        department: 'Beauty department',
        location: 'X: 31.25, Y: 16.5',
        alley: 'A07 14',
        imageHTML: <img name="image" style={{width: '200px', height: '200px', alignContent: 'center', marginLeft: '100px'}} src = {item3}/>,
    },
    {
        itemId: '04',
        itemName: 'Slider',
        SKU: '437987',
        department: 'Toy department',
        location: 'X: 39.0, Y: 12.0',
        alley: 'A05 07',
        imageHTML: <img name="image" style={{width: '200px', height: '200px', alignContent: 'center', marginLeft: '100px'}} src = {item4}/>,
    },
  ]
  

    const [employeeData, setEmployeeData] = React.useState(data)
  
    const onChange = (e, itemId) => {
      const { itemName, value } = e.target
  
      const editData = employeeData.map((item) =>
        item.itemId === itemId && itemName ? { ...item, [itemName]: value } : item
      )
  
      setEmployeeData(editData)
    }

  
  
  

  return (<> <ButtonAppBar/>
  <div class="box offset-bottom-right-shadow"> 
  <h1 className="text-heading">
                Results Chart Route
            </h1>  
            <img name="image" style={{ height: '400px', width: '1000px', alignContent: 'center', marginLeft: '250px'}} src = {img1}/>
            <ResponsiveContainer width="100%" aspect={3}>
                <LineChart data={pdata} margin={{ left: 250 }}>
                    <CartesianGrid />
                    <XAxis dataKey="x" name="X - Co-Ordinate"
                        interval={'preserveStartEnd'} />
                    <YAxis></YAxis>
                    <Legend />
                    <Tooltip />
                    <Line dataKey="y" name="Y"
                        stroke="black" activeDot={{ r: 8 }} />
                    <Line dataKey="x-cord" name="X"
                        stroke="black" activeDot={{ r: 8 }} />
                </LineChart>
            </ResponsiveContainer>
            <div className="container">
        <h1 className="title" style={{color: 'black'}}>Picking Sequence Table</h1>
        <table>
          <thead>
            <tr>
              <th>Item Name</th>
              <th>SKU</th>
              <th>Department</th>
              <th>Location</th>
              <th>Aisle</th>
              <th>Image</th>
            </tr>
          </thead>
          <tbody>
            {employeeData.map(({ itemId, itemName, SKU, department, location, alley, imageHTML }) => (
              <tr key={itemId}>
                <td>
                  <input
                    name="itemName"
                    value={itemName}
                    type="text"
                    onChange={(e) => onChange(e, itemId)}
                    placeholder="Type Item Id"
                  />
                </td>
                <td>
                  <input
                    name="SKU"
                    value={SKU}
                    type="SKU"
                    onChange={(e) => onChange(e, itemId)}
                    placeholder="Type SKU"
                  />
                </td>
                <td>
                  <input
                    name="department"
                    type="text"
                    value={department}
                    onChange={(e) => onChange(e, itemId)}
                    placeholder="Type Department"
                  />
                </td>
                <td>
                  <input
                    name="location"
                    type="text"
                    value={location}
                    onChange={(e) => onChange(e, itemId)}
                    placeholder="Type Location"
                  />
                </td>
                <td>
                  <input
                    name="alley"
                    type="text"
                    value={alley}
                    onChange={(e) => onChange(e, itemId)}
                    placeholder="Type Alley"
                  />
                </td>
                <td>
                    {imageHTML}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
  </div>
</>
  );
}
