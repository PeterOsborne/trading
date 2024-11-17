import asyncio
import argparse
from streamers import stream_book_ticker, stream_depth
from data_manager import DataManager
from tabulate import tabulate


def display_order_book(top_of_book, order_book_depth):
    """Display the order book in the terminal."""
    print("\033[H\033[J", end="")  # Clear the screen

    best_bid_price = top_of_book.get("best_bid_price", "N/A")
    best_bid_qty = top_of_book.get("best_bid_qty", "N/A")
    best_ask_price = top_of_book.get("best_ask_price", "N/A")
    best_ask_qty = top_of_book.get("best_ask_qty", "N/A")

    # Calculate the spread
    if isinstance(best_bid_price, (float, int)) and isinstance(best_ask_price, (float, int)):
        spread = best_ask_price - best_bid_price
        formatted_spread = f"{spread:.10f}".rstrip("0").rstrip(".")  # Avoid scientific notation
    else:
        formatted_spread = "N/A"

    print("Top of Book @0ms:")
    top_of_book_table = [[
        f"{best_bid_price}, {best_bid_qty}",
        f"{best_ask_price}, {best_ask_qty}"
    ]]
    print(tabulate(top_of_book_table, headers=["Bids", "Asks"], tablefmt="grid"))

    # Display the spread
    print(f"\nSpread: {formatted_spread}\n")

    print("\nEntire Book @100ms:")
    max_rows = max(len(order_book_depth.get("bids", [])), len(order_book_depth.get("asks", [])))
    full_order_book_table = []
    for i in range(max_rows):
        bid = f"{order_book_depth['bids'][i][0]}, {order_book_depth['bids'][i][1]}" if i < len(order_book_depth["bids"]) else ""
        ask = f"{order_book_depth['asks'][i][0]}, {order_book_depth['asks'][i][1]}" if i < len(order_book_depth["asks"]) else ""
        full_order_book_table.append([bid, ask])
    print(tabulate(full_order_book_table, headers=["Bids", "Asks"], tablefmt="grid"))


async def main():
    """Main entry point for the terminal-based order book viewer."""
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Binance Order Book Viewer (Terminal)")
    parser.add_argument(
        "--env", choices=["testnet", "real"], default="testnet",
        help="Specify the environment: 'testnet' or 'real' (default: testnet)"
    )
    parser.add_argument(
        "--pair", required=True, help="Trading pair to monitor (e.g., DOGEUSDT)"
    )
    args = parser.parse_args()

    # Get configuration for the environment
    from config_manager import ConfigManager
    config_manager = ConfigManager()
    config = config_manager.get_config(args.env)

    # Initialize data manager to store order book data
    data_manager = DataManager()

    # Register `display_order_book` to update terminal whenever data changes
    data_manager.register_listener(display_order_book)

    # Start the WebSocket streams for top-of-book and full-depth
    await asyncio.gather(
        stream_book_ticker(config["ws_url"], args.pair.lower(), data_manager),
        stream_depth(config["ws_url"], args.pair.lower(), data_manager)
    )


if __name__ == "__main__":
    asyncio.run(main())
