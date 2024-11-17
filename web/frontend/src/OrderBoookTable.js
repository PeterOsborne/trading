import React from "react";

const OrderBookTable = ({ topOfBook, orderBookDepth }) => {
    return (
        <div>
            <h3>Top of Book</h3>
            <table>
                <thead>
                    <tr>
                        <th>Bids (Price, Qty)</th>
                        <th>Asks (Price, Qty)</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>{`${topOfBook.best_bid_price}, ${topOfBook.best_bid_qty}`}</td>
                        <td>{`${topOfBook.best_ask_price}, ${topOfBook.best_ask_qty}`}</td>
                    </tr>
                </tbody>
            </table>

            <h3>Order Book Depth</h3>
            <table>
                <thead>
                    <tr>
                        <th>Bids</th>
                        <th>Asks</th>
                    </tr>
                </thead>
                <tbody>
                    {Array.from({ length: Math.max(orderBookDepth.bids.length, orderBookDepth.asks.length) }).map((_, i) => (
                        <tr key={i}>
                            <td>{orderBookDepth.bids[i] ? `${orderBookDepth.bids[i][0]}, ${orderBookDepth.bids[i][1]}` : ""}</td>
                            <td>{orderBookDepth.asks[i] ? `${orderBookDepth.asks[i][0]}, ${orderBookDepth.asks[i][1]}` : ""}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default OrderBookTable;
