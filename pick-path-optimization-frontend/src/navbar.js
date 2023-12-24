import * as React from 'react';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import IconButton from '@mui/material/IconButton';
import Typography from '@mui/material/Typography';
import Menu from '@mui/material/Menu';
import MenuIcon from '@mui/icons-material/Menu';
import Container from '@mui/material/Container';
import Avatar from '@mui/material/Avatar';
import Button from '@mui/material/Button';
import Tooltip from '@mui/material/Tooltip';
import MenuItem from '@mui/material/MenuItem';
import AdbIcon from '@mui/icons-material/Adb';
import Link from '@mui/material/Link';
import Logo from "./nextuple.svg";
import { makeStyles } from "@material-ui/core/styles";


const pages = ['Wave-Simulation', 'Batch-Simulation'];

function ResponsiveAppBar() {
  const [anchorElNav, setAnchorElNav] = React.useState(null);
  const [anchorElUser, setAnchorElUser] = React.useState(null);

  const handleOpenNavMenu = (event) => {
    setAnchorElNav(event.currentTarget);
  };
  const handleOpenUserMenu = (event) => {
    setAnchorElUser(event.currentTarget);
  };

  const handleCloseNavMenu = () => {
    setAnchorElNav(null);
  };

  const handleCloseUserMenu = () => {
    setAnchorElUser(null);
  };
  const useStyles = makeStyles({
    logo: {
      maxWidth: 160,
    },
  });

  const classes = useStyles();

  return (
    <AppBar style={{ background: '#efefef' }} position="static">
      <Container maxWidth="xl">
        <Toolbar disableGutters>
          {/* <AdbIcon sx={{ display: { xs: 'none', md: 'flex' }, mr: 1 }} /> */}
          {/* <Typography
            variant="h6"
            noWrap
            component="a"
            href="/"
            sx={{
              mr: 2,
              display: { xs: 'none', md: 'flex' },
              fontFamily: 'monospace',
              fontWeight: 700,
              letterSpacing: '.3rem',
              color: 'black',
              textDecoration: 'none',
            }}
          >
            NEXTUPLE
          </Typography> */}
          <img src={Logo} sx={{justifyContent: "flex-end" }} alt="logo" className={classes.logo} />


          <Box style={{paddingLeft: '100px'}} sx={{ flexGrow: 1,  display: { xs: 'none', md: 'flex' } }}>
          <Button href="/route"sx={{ my: 3, color: 'black', fontFamily: 'Montserrat,sans-serif', fontSize: '19px', fontWeight: 600,  display: 'block' }}>Route-Simulation</Button>
          <Button href="/wave"sx={{ my: 3, color: 'black',  fontFamily: 'Montserrat,sans-serif', fontSize: '19px', fontWeight: 600, display: 'block' }}>Wave-Simulation</Button>
          <Button href="/batch"sx={{ my: 3, color: 'black', fontFamily: 'Montserrat,sans-serif', fontSize: '19px', fontWeight: 600, display: 'block' }}>Cluster-Simulation</Button>
         
        
          </Box>


        </Toolbar>
      </Container>
    </AppBar>
  );
}
export default ResponsiveAppBar;