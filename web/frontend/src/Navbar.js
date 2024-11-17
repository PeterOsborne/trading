import React from "react";
import { Link } from "react-router-dom";

const Navbar = () => {
    return (
        <nav className="navbar">
            <Link to="/testnet" className="nav-link">Testnet</Link>
            <Link to="/real" className="nav-link">Real</Link>
        </nav>
    );
};

export default Navbar;
