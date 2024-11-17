import asyncio
import argparse
import logging
import websockets
import json
import sys
import os

# Add the root directory to the Python module path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from streamers import stream_book_ticker, stream_depth
from data_manager import DataManager

# Initialize the logger
logging.basicConfig(level=logging.DEBUG)

# Data manager to manage shared data
data_manager = DataManager()

# WebSocket clients
websocket_clients = set()

async def broadcast_order_book():
    """Broadcast the latest order book to all connected WebSocket clients."""
    while True:
        if websocket_clients and data_manager.top_of_book and data_manager.order_book_depth:
            message = {
                "top_of_book": data_manager.top_of_book,
                "order_book_depth": data_manager.order_book_depth,
            }
            disconnected_clients = set()
            for client in websocket_clients:
                try:
                    await client.send(json.dumps(message))
                except websockets.exceptions.ConnectionClosed:
                    logging.warning("A WebSocket client disconnected.")
                    disconnected_clients.add(client)
            websocket_clients.difference_update(disconnected_clients)
        await asyncio.sleep(0.1)  # Broadcast every 100ms


async def websocket_handler(websocket):
    """Handle incoming WebSocket connections."""
    websocket_clients.add(websocket)
    logging.info("A new WebSocket client connected.")
    try:
        while True:
            await websocket.recv()  # Keep connection alive
    except websockets.exceptions.ConnectionClosed:
        logging.warning("WebSocket connection closed.")
    finally:
        websocket_clients.remove(websocket)


async def main():
    """Main entry point for the terminal-based order book viewer and WebSocket server."""
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Binance Order Book Viewer (Terminal + WebSocket)")
    parser.add_argument(
        "--env", choices=["testnet", "real"], default="testnet",
        help="Specify the environment: 'testnet' or 'real' (default: testnet)"
    )
    parser.add_argument(
        "--pair", required=True, help="Trading pair to monitor (e.g., DOGEUSDT)"
    )
    parser.add_argument(
        "--ws-port", type=int, default=8765, help="Port for the WebSocket server (default: 8765)"
    )
    args = parser.parse_args()

    # Get configuration for the environment
    from config_manager import ConfigManager
    config_manager = ConfigManager()
    config = config_manager.get_config(args.env)

    # Start WebSocket server
    websocket_server = websockets.serve(websocket_handler, "0.0.0.0", args.ws_port)

    # Start broadcasting data to WebSocket clients
    asyncio.create_task(broadcast_order_book())

    # Start the Binance WebSocket streams
    await asyncio.gather(
        websocket_server,
        stream_book_ticker(config["ws_url"], args.pair.lower(), data_manager),
        stream_depth(config["ws_url"], args.pair.lower(), data_manager),
    )


if __name__ == "__main__":
    asyncio.run(main())
