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

export default function RangeSliderWave() {
  var timeout;
  const classes = useStyles();
  const [value, setValue] = React.useState(0);
  const [OrderLines,setOrderLines]=React.useState(0);
  const [n1, setN1] = React.useState(1);
  const [n2, setN2] = React.useState(10);
  const [result, setResult] = React.useState({});
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

  const handleSubmit = async(e) => {
    e.preventDefault();
    console.log(OrderLines);
    console.log(n1);
    console.log(n2);

      axios.post("http://localhost:5000/simulate-n-wave-orders",null,{ params: {
        n1:n1,n2:n2,lines_number:OrderLines,y_low:5.5,y_high:50
      }})
    .then((response) => {
      console.log(response.data);
      setResult(response.data)
      navigate('/result', {state: response.data })
    }).catch(e => {
      console.log(e);
  });
  }

  return (<>  
  
  <ButtonAppBar/>  
  <main alignItems="center" class="hero-section-new">
  <div className={classes.root}>
    <Typography style={{ color: 'black' , marginLeft: '50px', paddingTop: '120px', fontWeight: 600, fontSize: '18px'}} id="range-slider" gutterBottom>
      Select OrderLines Range for Wave Simulation
    </Typography>
    <Slider style={{ marginTop: '35px' }}
    className="customSlider"
      min={0}
      max={2000}
      value={value}
      onChange={handleChange}
      onChangeCommitted={handleChangeCommitted}
      valueLabelDisplay="on"
      aria-labelledby="range-slider"
      getAriaValueText={valuetext}
    />
<Grid container direction={"column"} spacing={4} alignItems="center">
<Grid item>
  <TextField label="N_MIN" variant="outlined" 
  defaultValue="1" helperText="Orders/Wave"
  margin="dense" 
  className="searchBar"
  style = {{width: 250}}
  onChange={e => setN1(e.target.value)}/>
</Grid>
<Grid item>
<TextField label="N_MAX" variant="outlined" 
  defaultValue="5" helperText="Orders/Wave"
  margin="dense" 
  style = {{width: 250}}
  onChange={e => setN2(e.target.value)}/>
</Grid>
{/* <Grid item>
  <TextField label="DISTANCE_THRESHOLD" 
  defaultValue="35" helperText="Distance in meters"
  margin="dense"
  style = {{width: 250}}
  variant="outlined" onChange={e => setDist(e.target.value)}/>
</Grid> */}
<Button style={{background: '#2f91d5'}} variant="contained" endIcon={<SendIcon />} padding="10px" onClick={handleSubmit} fullWidth>
Calculate
</Button>
</Grid>
  </div>
  </main>
  </>
  );
}