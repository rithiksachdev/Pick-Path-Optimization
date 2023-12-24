import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import Typography from "@material-ui/core/Typography";
import Slider from "@material-ui/core/Slider";
import axios from "axios";
import SendIcon from '@mui/icons-material/Send'
import "./Slider.css"
import ButtonAppBar from './navbar';
import { TextField,Grid, Button, Icon, Paper } from "@material-ui/core";
import { useNavigate } from 'react-router-dom';
  

const useStyles = makeStyles({
  root: {
    marginLeft: '34%',
    marginRight: 50,
    padding: '0 30px',
    width: 500,
    alignItems: "center",
    justifyContent: "center",
    button: {
      margin: 1
    },
    leftIcon: {
      marginRight: 1
    },
    rightIcon: {
      marginLeft: 1
    }
  },
});

function valuetext(value) {
  return `${value}`;
}

export default function RouteSimulation() {
  var timeout;
  const classes = useStyles();
  const [value, setValue] = React.useState(0);
  const [OrderLines,setOrderLines]=React.useState(0);
  const [n1, setN1] = React.useState(1);
  const [n2, setN2] = React.useState(10);
  const [dist, setDist] = React.useState(35);
  const [orderId, setOrderId] = React.useState(35);
  const handleChange = (event, newValue) => {
    timeout && clearTimeout(timeout);
    timeout = setTimeout(() => {
      setValue(newValue); 
      setOrderLines(newValue);
      
    }, 1);
  };
  const handleVariableChange = (event) => {
    setN1(event.target.value);
    //console.log(n1)
  };


  const handleChangeCommitted = (event, newValue) => {
    //console.log(newValue)
    // console.log(newValue)
  //   axios.post("http://localhost:5000/simulate-n-batch-orders",null,{ params: {
  //       n1:n1,n2:10,lines_number:newValue,y_low:5.5,y_high:50,distance_threshold:35
  //     }})
  //   .then((response) => {
  //     console.log(response.data);
  //   }).catch(e => {
  //     console.log(e);
  // });
  }
  const navigate = useNavigate();

  let handleSubmit = async (e) => {
    e.preventDefault();
    console.log(OrderLines);
    console.log(n1);
    console.log(n2);
    console.log(dist);
      axios.post("http://localhost:5000/get-route-new",null,{ params: {
        n1:1,n2:5,lines_number:5000,y_low:5.5,y_high:50, orderId: orderId
      }})
    .then((response) => {
      console.log(response.data);
      navigate('/resultRoute', {state: response.data })
    }).catch(e => {
      console.log(e);
  });
  }

  return (<> <ButtonAppBar/>
  <main alignItems="center" class="hero-section-new">
    <div className={classes.root}>  
    <Typography style={{ color: 'black' , marginLeft: '60px', paddingTop: '120px', fontWeight: 600, fontSize: '18px', marginBottom: '15px'}} id="range-slider" gutterBottom>
      Give Order Number for Route Simulation:
    </Typography>
    
<Grid container direction={"column"} spacing={4} alignItems="center">
{/* <Grid item>
  <TextField label="N_MIN" id="outlined-margin-dense" className={classes.textField} defaultValue="1" helperText="Orders/Wave" margin="dense" variant="outlined" onChange={e => setN1(e.target.value)}/>
</Grid>
<Grid item>
  <TextField label="N_MAX" id="outlined-margin-dense" className={classes.textField} defaultValue="5" helperText="Orders/Wave" margin="dense" variant="outlined" onChange={e => setN2(e.target.value)}/>
</Grid> */}
{/* <Grid item>
  <TextField label="DISTANCE_THRESHOLD" id="outlined-margin-dense" className={classes.textField} defaultValue="35" helperText="Distance in meters" margin="dense" variant="outlined" onChange={e => setDist(e.target.value)}/>
</Grid> */}
<Grid item>
  <TextField label="ORDER_NUMBER" id="outlined-margin-dense" className={classes.textField}  margin="dense" variant="outlined" onChange={e => setOrderId(e.target.value)}/>
</Grid>
<Button style={{background: '#2f91d5'}} variant="contained" endIcon={<SendIcon />} padding="10px" onClick={handleSubmit} fullWidth>
Calculate
</Button>
</Grid>
  </div>
  </main>
</>
  );
}
