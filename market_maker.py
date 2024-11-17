import asyncio
import argparse
from data_manager import DataManager
from streamers import stream_book_ticker, stream_depth
from binance.client import Client
from utils import load_api_keys, get_tick_size
from order_manager import OrderManager

def submit_orders(top_of_book, order_book_depth):
    """Perform order submission logic."""
    # Initialize client
    client = Client(API_KEY, API_SECRET, testnet=(env == "testnet"))

    # Initialize OrderManager
    order_manager = OrderManager(client, top_of_book["symbol"])

    # Get current position using OrderManager
    
    
    
    
    
    # ISSUE IS HERE
    position = order_manager.get_position()
    print(f"Current Position: {position}")








    # Get current orders using OrderManager
    current_orders = order_manager.get_active_orders()
    print(f"Current Orders: {current_orders}")
    
    # Get tick size for the trading pair
    tick_size = get_tick_size(client, top_of_book["symbol"])
    if tick_size is None:
        print(f"Unable to retrieve tick size for {top_of_book['symbol']}.")
        return

    # Define order parameters
    desired_order_size = 100  # Desired total order size
    spread = 0.001            # Spread as a fraction of price

    best_bid_price = float(top_of_book.get("best_bid_price", 0))
    best_ask_price = float(top_of_book.get("best_ask_price", 0))

    # Ensure we have valid top-of-book data
    if best_bid_price <= 0 or best_ask_price <= 0:
        print("Invalid top-of-book data.")
        return

    # Calculate bid and ask prices, rounded to the tick size
    best_bid_price = float(top_of_book.get("best_bid_price", 0))
    best_ask_price = float(top_of_book.get("best_ask_price", 0))
    if best_bid_price == 0 or best_ask_price == 0:
        return

    # Check if current orders are at the top of the order book
    existing_bid = next((o for o in current_orders if o['side'] == 'BUY' and float(o['price']) == best_bid_price), None)
    existing_ask = next((o for o in current_orders if o['side'] == 'SELL' and float(o['price']) == best_ask_price), None)

    # Calculate remaining sizes for each side
    remaining_bid_size = desired_order_size
    if existing_bid:
        existing_bid_size = float(existing_bid['origQty']) - float(existing_bid['executedQty'])
        remaining_bid_size = max(0, desired_order_size - existing_bid_size)

    remaining_ask_size = desired_order_size
    if existing_ask:
        existing_ask_size = float(existing_ask['origQty']) - float(existing_ask['executedQty'])
        remaining_ask_size = max(0, desired_order_size - existing_ask_size)

    # Place an additional buy order for the remaining size, if necessary
    if remaining_bid_size > 0:
        order_manager.place_order('BUY', best_bid_price, remaining_bid_size)

    # Place an additional sell order for the remaining size, if necessary
    if remaining_ask_size > 0:
        order_manager.place_order('SELL', best_ask_price, remaining_ask_size)




async def main():
    parser = argparse.ArgumentParser(description="Binance Market Maker")
    parser.add_argument(
        "--env", choices=["testnet", "real"], default="testnet",
        help="Specify the environment: 'testnet' or 'real' (default: testnet)"
    )
    parser.add_argument(
        "--pair", required=True, help="Trading pair to monitor (e.g., DOGEUSDT)"
    )
    args = parser.parse_args()

    # Load API keys
    global API_KEY, API_SECRET, env
    env = args.env
    API_KEY, API_SECRET = load_api_keys(env)

    # Initialize Binance client
    client = Client(API_KEY, API_SECRET, testnet=(env == "testnet"))

    from config_manager import ConfigManager
    config_manager = ConfigManager()
    config = config_manager.get_config(env)

    data_manager = DataManager()
    data_manager.register_listener(submit_orders)

    print(args.pair)
    await asyncio.gather(
        stream_book_ticker(config["ws_url"], args.pair.lower(), data_manager),
        stream_depth(config["ws_url"], args.pair.lower(), data_manager)
    )

if __name__ == "__main__":
    asyncio.run(main())
