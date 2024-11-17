import asyncio
import argparse
import logging
import websockets
import json
import sys
import os
from urllib.parse import urlparse, parse_qs

# Add the root directory to the Python module path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from streamers import stream_book_ticker, stream_depth
from data_manager import DataManager

# Initialize the logger
logging.basicConfig(level=logging.DEBUG)

# Data manager instances for managing data per pair
data_managers = {}

# WebSocket clients
websocket_clients = {}


async def broadcast_order_book(pair):
    """Broadcast the latest order book to all connected WebSocket clients for the given trading pair."""
    while True:
        if pair in websocket_clients and websocket_clients[pair]:
            data_manager = data_managers.get(pair)
            if data_manager and data_manager.top_of_book and data_manager.order_book_depth:
                message = {
                    "top_of_book": data_manager.top_of_book,
                    "order_book_depth": data_manager.order_book_depth,
                }
                disconnected_clients = set()
                for client in websocket_clients[pair]:
                    try:
                        await client.send(json.dumps(message))
                    except websockets.exceptions.ConnectionClosed:
                        logging.warning(f"A WebSocket client disconnected for pair: {pair}")
                        disconnected_clients.add(client)
                websocket_clients[pair].difference_update(disconnected_clients)
        await asyncio.sleep(0.1)  # Broadcast every 100ms


async def websocket_handler(websocket, path):
    """Handle incoming WebSocket connections."""
    query = parse_qs(urlparse(path).query)
    pair = query.get("pair", ["BTCUSDT"])[0].upper()  # Default to BTCUSDT

    logging.info(f"New WebSocket client connected for pair: {pair}")

    # Add the client to the set for this trading pair
    if pair not in websocket_clients:
        websocket_clients[pair] = set()
    websocket_clients[pair].add(websocket)

    # Ensure a DataManager exists for the pair
    if pair not in data_managers:
        data_managers[pair] = DataManager()
        asyncio.create_task(start_binance_streams(pair))

    try:
        while True:
            await websocket.recv()  # Keep connection alive
    except websockets.exceptions.ConnectionClosed:
        logging.warning(f"WebSocket connection closed for pair: {pair}")
    finally:
        websocket_clients[pair].remove(websocket)


async def start_binance_streams(pair):
    """Start Binance WebSocket streams for the given trading pair."""
    env = "testnet"  # Modify this if needed for real environment
    from config_manager import ConfigManager
    config_manager = ConfigManager()
    config = config_manager.get_config(env)

    data_manager = data_managers[pair]
    logging.info(f"Starting Binance WebSocket streams for pair: {pair}")

    await asyncio.gather(
        stream_book_ticker(config["ws_url"], pair.lower(), data_manager),
        stream_depth(config["ws_url"], pair.lower(), data_manager),
        broadcast_order_book(pair),
    )


async def main():
    """Main entry point for the terminal-based order book viewer and WebSocket server."""
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Binance Order Book Viewer (WebSocket)")
    parser.add_argument(
        "--env", choices=["testnet", "real"], default="testnet",
        help="Specify the environment: 'testnet' or 'real' (default: testnet)"
    )
    parser.add_argument(
        "--pair", default="BTCUSDT", help="Default trading pair to monitor (e.g., DOGEUSDT)"
    )
    parser.add_argument(
        "--ws-port", type=int, default=8765, help="Port for the WebSocket server (default: 8765)"
    )
    args = parser.parse_args()

    # Get configuration for the environment
    from config_manager import ConfigManager
    config_manager = ConfigManager()
    config = config_manager.get_config(args.env)

    # Create a DataManager for the default pair and start Binance streams
    default_pair = args.pair.upper()
    data_managers[default_pair] = DataManager()
    asyncio.create_task(start_binance_streams(default_pair))

    # Start WebSocket server
    websocket_server = websockets.serve(websocket_handler, "0.0.0.0", args.ws_port)
    logging.info(f"WebSocket server running on port {args.ws_port}")

    # Start the Binance WebSocket streams and WebSocket server
    await asyncio.gather(
        websocket_server,
        stream_book_ticker(config["ws_url"], default_pair.lower(), data_managers[default_pair]),
        stream_depth(config["ws_url"], default_pair.lower(), data_managers[default_pair]),
    )


if __name__ == "__main__":
    asyncio.run(main())
