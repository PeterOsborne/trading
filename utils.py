from binance.client import Client

API_KEY = None
API_SECRET = None

def load_api_keys(env):
    """Load API keys from the secrets file."""
    global API_KEY, API_SECRET
    secrets_file = "binance_secrets.txt"
    keys = {}

    with open(secrets_file, "r") as f:
        for line in f:
            key, value = line.strip().split("=")
            keys[key] = value

    if env == "testnet":
        API_KEY = keys["TESTNET_API_KEY"]
        API_SECRET = keys["TESTNET_API_SECRET"]
    elif env == "real":
        API_KEY = keys["REAL_API_KEY"]
        API_SECRET = keys["REAL_API_SECRET"]

    return API_KEY, API_SECRET


def get_tick_size(client, trading_pair):
    """
    Get the tick size for a given trading pair on Binance.

    Args:
        client (binance.client.Client): The initialized Binance client.
        trading_pair (str): The trading pair (e.g., "BTCUSDT").

    Returns:
        float: The tick size for the trading pair.
    """
    try:
        # Fetch symbol information from Binance API
        symbol_info = client.get_symbol_info(trading_pair)
        if not symbol_info:
            raise ValueError(f"Trading pair {trading_pair} not found on Binance.")
        
        # Extract the tick size from the PRICE_FILTER
        for filter in symbol_info["filters"]:
            if filter["filterType"] == "PRICE_FILTER":
                return float(filter["tickSize"])

        # If no PRICE_FILTER is found, raise an exception
        raise ValueError(f"No PRICE_FILTER found for trading pair {trading_pair}.")

    except Exception as e:
        print(f"Error fetching tick size: {e}")
        return None


def format_price(price, precision=6):
    """Format price to show a fixed number of decimal places."""
    return f"{price:.{precision}f}"
