import asyncio
import websockets
import json
from tabulate import tabulate
import argparse
import os


def load_secrets(file_path="binance_secrets.txt"):
    """Load API keys and secrets from a file."""
    secrets = {}
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Secret file not found: {file_path}")
    with open(file_path, "r") as file:
        for line in file:
            # Skip empty lines and lines without '='
            if "=" in line:
                key, value = line.strip().split("=", 1)
                secrets[key] = value
    return secrets


def get_config(env):
    """Return configuration based on environment (testnet or real market)."""
    secrets = load_secrets()  # Load secrets from the file
    try:
        if env == "testnet":
            return {
                "ws_url": "wss://testnet.binance.vision/ws",
                "base_url": "https://testnet.binance.vision/api",
                "api_key": secrets["TESTNET_API_KEY"],
                "api_secret": secrets["TESTNET_API_SECRET"],
            }
        elif env == "real":
            return {
                "ws_url": "wss://stream.binance.com:9443/ws",
                "base_url": "https://api.binance.com/api",
                "api_key": secrets["REAL_API_KEY"],
                "api_secret": secrets["REAL_API_SECRET"],
            }
        else:
            raise ValueError("Invalid environment. Use 'testnet' or 'real'.")
    except KeyError as e:
        raise ValueError(f"Missing key in secrets file: {e}")


def format_price(price):
    """Format price to always show 6 decimal places."""
    return f"{price:.6f}"


async def connect_and_stream_order_book(ws_url, symbol, env):
    """Connect to Binance WebSocket and stream live order book data."""
    url = f"{ws_url}/{symbol}@depth5"  # Stream order book depth (top 5 levels)
    async with websockets.connect(url) as websocket:
        print(f"Connected to Binance WebSocket for {symbol.upper()} order book.")

        try:
            while True:
                # Receive a message from the WebSocket
                message = await websocket.recv()
                data = json.loads(message)

                # Extract bids and asks from the order book
                bids = [[format_price(float(b[0])), float(b[1])] for b in data["bids"]]
                asks = [[format_price(float(a[0])), float(a[1])] for a in data["asks"]]

                # Prepare data for display
                max_rows = max(len(bids), len(asks))
                order_book_table = []

                for i in range(max_rows):
                    bid = f"{bids[i][0]}, {bids[i][1]:.4f}" if i < len(bids) else ""
                    ask = f"{asks[i][0]}, {asks[i][1]:.4f}" if i < len(asks) else ""
                    order_book_table.append([bid, ask])

                # Display the order book
                # Clear the terminal for real-time updates
                print("\033[H\033[J", end="")
                print(f"Order Book (DOGE/USDT) - {'LIVE' if env == 'real' else 'TEST'} Environment:\n")
                print(tabulate(
                    order_book_table,
                    headers=["Bids (Price, Quantity)", "Asks (Price, Quantity)"],
                    tablefmt="grid",
                ))

                # Small delay to avoid overwhelming the terminal
                await asyncio.sleep(0.1)

        except websockets.exceptions.ConnectionClosed as e:
            print(f"WebSocket connection closed: {e}")
        except Exception as e:
            print(f"Error: {e}")


async def main():
    """Main entry point for the WebSocket connection."""
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Binance Order Book Monitor")
    parser.add_argument(
        "--env", choices=["testnet", "real"], default="testnet",
        help="Specify the environment: 'testnet' or 'real' (default: testnet)"
    )
    args = parser.parse_args()

    # Get configuration based on the environment
    config = get_config(args.env)

    # Connect and stream order book
    await connect_and_stream_order_book(config["ws_url"], TRADING_PAIR, args.env)


if __name__ == "__main__":
    # Trading pair to monitor
    TRADING_PAIR = "dogeusdt"
    asyncio.run(main())
