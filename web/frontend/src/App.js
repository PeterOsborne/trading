import React from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import Testnet from "./pages/Testnet";
import Real from "./pages/Real";
import { AppBar, Toolbar, Typography, Button, Box } from "@mui/material";

const App = () => {
  return (
    <Router>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" sx={{ flexGrow: 1 }}>
            Binance Order Book
          </Typography>
          <Button color="inherit" component={Link} to="/">
            Testnet
          </Button>
          <Button color="inherit" component={Link} to="/real">
            Real
          </Button>
        </Toolbar>
      </AppBar>
      <Box mt={4}>
        <Routes>
          <Route path="/" element={<Testnet />} />
          <Route path="/real" element={<Real />} />
        </Routes>
      </Box>
    </Router>
  );
};

export default App;
