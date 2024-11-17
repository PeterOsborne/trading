import React, { useState, useEffect } from "react";
import {
    Typography,
    Box,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    Paper,
    Grid,
    TextField,
    Button,
} from "@mui/material";

const Testnet = () => {
    const [pair, setPair] = useState("BTCUSDT"); // Default market
    const [searchInput, setSearchInput] = useState("");
    const [orderBook, setOrderBook] = useState({
        top_of_book: {},
        order_book_depth: { bids: [], asks: [] },
    });

    useEffect(() => {
        const ws = new WebSocket(`ws://localhost:8765?pair=${pair}`); // Pass the selected pair to the backend

        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            setOrderBook(data);
        };

        return () => ws.close();
    }, [pair]); // Reconnect WebSocket when the pair changes

    const handleSearchSubmit = () => {
        if (searchInput.trim()) {
            setPair(searchInput.toUpperCase());
            setSearchInput(""); // Clear the input field
        }
    };

    const { top_of_book, order_book_depth } = orderBook;

    // Calculate the spread
    const spread =
        top_of_book.best_ask_price && top_of_book.best_bid_price
            ? (top_of_book.best_ask_price - top_of_book.best_bid_price).toFixed(8)
            : "N/A";

    return (
        <Box p={4}>
            <Typography variant="h3" align="center" gutterBottom>
                {`Testnet Order Book - ${pair}`}
            </Typography>

            <Box mt={2} display="flex" justifyContent="center">
                <TextField
                    label="Enter Market (e.g., BTCUSDT)"
                    value={searchInput}
                    onChange={(e) => setSearchInput(e.target.value)}
                    variant="outlined"
                    sx={{ mr: 2 }}
                />
                <Button variant="contained" color="primary" onClick={handleSearchSubmit}>
                    Search
                </Button>
            </Box>

            <Box mt={4}>
                <Typography variant="h5">Top of Book</Typography>
                <TableContainer component={Paper} sx={{ mt: 2 }}>
                    <Table>
                        <TableHead>
                            <TableRow>
                                <TableCell align="center"><b>Type</b></TableCell>
                                <TableCell align="center"><b>Price</b></TableCell>
                                <TableCell align="center"><b>Quantity</b></TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            <TableRow>
                                <TableCell align="center">Best Bid</TableCell>
                                <TableCell align="center">{top_of_book.best_bid_price || "N/A"}</TableCell>
                                <TableCell align="center">{top_of_book.best_bid_qty || "N/A"}</TableCell>
                            </TableRow>
                            <TableRow>
                                <TableCell align="center">Best Ask</TableCell>
                                <TableCell align="center">{top_of_book.best_ask_price || "N/A"}</TableCell>
                                <TableCell align="center">{top_of_book.best_ask_qty || "N/A"}</TableCell>
                            </TableRow>
                            <TableRow>
                                <TableCell align="center" colSpan={2}><b>Spread</b></TableCell>
                                <TableCell align="center">{spread}</TableCell>
                            </TableRow>
                        </TableBody>
                    </Table>
                </TableContainer>
            </Box>

            <Box mt={6}>
                <Typography variant="h5">Order Book Depth</Typography>
                <Grid container spacing={4} mt={2}>
                    {/* Bids Table */}
                    <Grid item xs={12} md={6}>
                        <Typography variant="h6" align="center">
                            Bids
                        </Typography>
                        <TableContainer component={Paper}>
                            <Table>
                                <TableHead>
                                    <TableRow>
                                        <TableCell align="center"><b>Quantity</b></TableCell>
                                        <TableCell align="center"><b>Price</b></TableCell>
                                    </TableRow>
                                </TableHead>
                                <TableBody>
                                    {order_book_depth.bids.map((bid, index) => (
                                        <TableRow key={index}>
                                            <TableCell align="center">{bid[1]}</TableCell>
                                            <TableCell align="center">{bid[0]}</TableCell>
                                        </TableRow>
                                    ))}
                                </TableBody>
                            </Table>
                        </TableContainer>
                    </Grid>

                    {/* Asks Table */}
                    <Grid item xs={12} md={6}>
                        <Typography variant="h6" align="center">
                            Asks
                        </Typography>
                        <TableContainer component={Paper}>
                            <Table>
                                <TableHead>
                                    <TableRow>
                                        <TableCell align="center"><b>Price</b></TableCell>
                                        <TableCell align="center"><b>Quantity</b></TableCell>
                                    </TableRow>
                                </TableHead>
                                <TableBody>
                                    {order_book_depth.asks.map((ask, index) => (
                                        <TableRow key={index}>
                                            <TableCell align="center">{ask[0]}</TableCell>
                                            <TableCell align="center">{ask[1]}</TableCell>
                                        </TableRow>
                                    ))}
                                </TableBody>
                            </Table>
                        </TableContainer>
                    </Grid>
                </Grid>
            </Box>
        </Box>
    );
};

export default Testnet;
