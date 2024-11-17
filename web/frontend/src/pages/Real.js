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
} from "@mui/material";

const Testnet = () => {
    const [orderBook, setOrderBook] = useState({
        top_of_book: {},
        order_book_depth: { bids: [], asks: [] },
    });

    useEffect(() => {
        const ws = new WebSocket("ws://localhost:8766"); // Update port if needed

        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            setOrderBook(data);
        };

        return () => ws.close();
    }, []);

    const { top_of_book, order_book_depth } = orderBook;

    // Calculate the spread
    const bestBidPrice = parseFloat(top_of_book.best_bid_price || 0);
    const bestAskPrice = parseFloat(top_of_book.best_ask_price || 0);
    const spread = bestAskPrice && bestBidPrice ? (bestAskPrice - bestBidPrice).toFixed(6) : "N/A";

    return (
        <Box p={4}>
            <Typography variant="h3" align="center" gutterBottom>
                Testnet Order Book
            </Typography>

            {/* Spread Section */}
            <Box mt={2} mb={4} textAlign="center">
                <Typography variant="h5" gutterBottom>
                    Spread: {spread}
                </Typography>
            </Box>

            {/* Top of Book */}
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
                        </TableBody>
                    </Table>
                </TableContainer>
            </Box>

            {/* Order Book Depth */}
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
