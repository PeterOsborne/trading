import argparse
from config_manager import ConfigManager
from rest_api_manager import BinanceRestAPI


def neutralise_position(env, trading_pair):
    """Neutralise the position for the given trading pair."""
    try:
        # Load configuration based on the environment
        config_manager = ConfigManager()
        config = config_manager.get_config(env)

        # Initialise the Binance REST API wrapper
        rest_api = BinanceRestAPI(config["base_url"], config["api_key"], config["api_secret"])

        # Fetch the current balance for the base asset
        balances = rest_api.get_account_balance()
        base_asset = trading_pair[:-4]  # Extract base asset (e.g., DOGE from DOGEUSDT)
        base_balance = float(next((b["free"] for b in balances["balances"] if b["asset"] == base_asset), 0.0))
        print(f"Current {base_asset} balance: {base_balance:.4f}")

        # Neutralise position
        if base_balance > 0:
            print(f"Selling {base_balance:.4f} {base_asset} to neutralise position...")
            response = rest_api.place_market_order(symbol=trading_pair, side="SELL", quantity=base_balance)
            print(f"Order placed: {response}")
        elif base_balance < 0:
            print(f"Buying {abs(base_balance):.4f} {base_asset} to neutralise position...")
            response = rest_api.place_market_order(symbol=trading_pair, side="BUY", quantity=abs(base_balance))
            print(f"Order placed: {response}")
        else:
            print(f"Position is already neutral for {base_asset}.")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Neutralise Binance Position")
    parser.add_argument("--pair", required=True, help="Trading pair (e.g., DOGEUSDT)")
    parser.add_argument(
        "--env", choices=["testnet", "real"], default="testnet",
        help="Environment: testnet or real (default: testnet)"
    )
    args = parser.parse_args()

    neutralise_position(args.env, args.pair)
