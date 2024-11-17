import asyncio
import argparse
from config_manager import ConfigManager
from web_socket_wrapper import BinanceWebSocket
from utils import format_price
from tabulate import tabulate

async def connect_and_stream_order_book(ws_url, symbol, env):
    """Connect to Binance WebSocket and stream live order book data."""
    ws = BinanceWebSocket(ws_url, symbol)

    # Await the WebSocket connection
    websocket = await ws.connect()
    print(f"Connected to Binance WebSocket for {symbol.upper()} order book.")

    try:
        while True:
            # Receive a message from the WebSocket
            data = await ws.receive_order_book(websocket)

            # Extract bids and asks from the order book
            bids = [[format_price(float(b[0])), float(b[1])] for b in data["bids"]]
            asks = [[format_price(float(a[0])), float(a[1])] for a in data["asks"]]

            # Prepare data for display
            max_rows = max(len(bids), len(asks))
            order_book_table = []
            spread = float(asks[0][0]) - float(bids[0][0])

            for i in range(max_rows):
                bid = f"{bids[i][0]}, {bids[i][1]:.4f}" if i < len(bids) else ""
                ask = f"{asks[i][0]}, {asks[i][1]:.4f}" if i < len(asks) else ""
                order_book_table.append([bid, ask])

            # Display the order book
            # Clear the terminal for real-time updates
            print("\033[H\033[J", end="")
            print(f"Order Book ({symbol.upper()}) - {'LIVE' if env == 'real' else 'TEST'} Environment:\n")
            print(tabulate(
                order_book_table,
                headers=["Bids (Price, Quantity)", "Asks (Price, Quantity)"],
                tablefmt="grid",
            ))
            print(f"\nSpread: {f'{spread:.10f}'.rstrip('0').rstrip('.')}")

            # Small delay to avoid overwhelming the terminal
            await asyncio.sleep(0.1)

    except asyncio.CancelledError:
        print("WebSocket connection cancelled.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await websocket.close()


async def main():
    """Main entry point for the WebSocket connection."""
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Binance Order Book Monitor")
    parser.add_argument(
        "--env", choices=["testnet", "real"], default="testnet",
        help="Specify the environment: 'testnet' or 'real' (default: testnet)"
    )
    parser.add_argument(
        "--pair", required=True, help="Trading pair to monitor (e.g., DOGEUSDT)"
    )
    args = parser.parse_args()

    # Get configuration based on the environment
    config_manager = ConfigManager()
    config = config_manager.get_config(args.env)

    # Connect and stream order book
    await connect_and_stream_order_book(config["ws_url"], args.pair.lower(), args.env)


if __name__ == "__main__":
    asyncio.run(main())
