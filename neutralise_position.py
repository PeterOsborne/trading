import requests
import hmac
import hashlib
import time
import os
import argparse


def load_secrets(file_path="binance_secrets.txt"):
    """Load API key and secret from a file."""
    secrets = {}
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Secret file not found: {file_path}")
    with open(file_path, "r") as file:
        for line in file:
            key, value = line.strip().split("=", 1)
            secrets[key] = value
    return secrets


def get_config(env):
    """Return configuration based on environment (testnet or real market)."""
    secrets = load_secrets()
    try:
        if env == "testnet":
            return {
                "base_url": "https://testnet.binance.vision/api",
                "api_key": secrets["TESTNET_API_KEY"],
                "api_secret": secrets["TESTNET_API_SECRET"],
            }
        elif env == "real":
            return {
                "base_url": "https://api.binance.com/api",
                "api_key": secrets["REAL_API_KEY"],
                "api_secret": secrets["REAL_API_SECRET"],
            }
        else:
            raise ValueError("Invalid environment. Use 'testnet' or 'real'.")
    except KeyError as e:
        raise ValueError(f"Missing key in secrets file: {e}")


def create_signature(query_string, api_secret):
    """Create HMAC SHA256 signature."""
    return hmac.new(
        api_secret.encode("utf-8"),
        query_string.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()


def fetch_balance(base_url, api_key, api_secret, trading_pair):
    """Fetch account balance via REST API."""
    headers = {"X-MBX-APIKEY": api_key}

    # Generate the query string with a timestamp
    timestamp = int(time.time() * 1000)
    query_string = f"timestamp={timestamp}"
    signature = create_signature(query_string, api_secret)
    query_string += f"&signature={signature}"

    response = requests.get(f"{base_url}/v3/account?{query_string}", headers=headers)
    response.raise_for_status()  # Raise an error if the request failed

    # Parse the balances
    base_asset = trading_pair[:-4]  # Extract base asset from the trading pair (e.g., DOGE from DOGEUSDT)
    balances = response.json().get("balances", [])
    asset_balance = next((b for b in balances if b["asset"] == base_asset), {"free": "0.0"})
    return float(asset_balance["free"])


def place_market_order(base_url, api_key, api_secret, side, trading_pair, quantity):
    """Place a market order via REST API."""
    headers = {"X-MBX-APIKEY": api_key}

    # Generate the query string with timestamp and parameters
    timestamp = int(time.time() * 1000)
    query_string = (
        f"symbol={trading_pair}&side={side}&type=MARKET&quantity={quantity}&timestamp={timestamp}"
    )
    signature = create_signature(query_string, api_secret)
    query_string += f"&signature={signature}"

    response = requests.post(f"{base_url}/v3/order", headers=headers, params=query_string)
    response.raise_for_status()  # Raise an error if the request failed

    return response.json()


def neutralize_position(env, trading_pair):
    """Neutralize the position for the trading pair."""
    try:
        # Get configuration based on the environment
        config = get_config(env)
        base_url = config["base_url"]
        api_key = config["api_key"]
        api_secret = config["api_secret"]

        # Fetch the current balance for the base asset
        base_balance = fetch_balance(base_url, api_key, api_secret, trading_pair)
        print(f"Current {trading_pair[:-4]} balance: {base_balance:.4f}")

        if base_balance > 0:
            print(f"Selling {trading_pair[:-4]} to neutralize position...")
            response = place_market_order(base_url, api_key, api_secret, "SELL", trading_pair, base_balance)
        elif base_balance < 0:
            print(f"Buying {trading_pair[:-4]} to neutralize position...")
            response = place_market_order(base_url, api_key, api_secret, "BUY", trading_pair, abs(base_balance))
        else:
            print("Position already neutral.")
            return

        print(f"Order placed: {response}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Neutralize Binance Position")
    parser.add_argument("--pair", required=True, help="Trading pair (e.g., DOGEUSDT)")
    parser.add_argument(
        "--env", choices=["testnet", "real"], default="testnet", help="Environment: testnet or real (default: testnet)"
    )
    args = parser.parse_args()

    neutralize_position(args.env, args.pair)
