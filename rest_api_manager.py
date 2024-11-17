import requests
import time
import hmac
import hashlib


class BinanceRestAPI:
    """Simplified wrapper for Binance REST API requests."""

    def __init__(self, base_url, api_key, api_secret):
        self.base_url = base_url
        self.api_key = api_key
        self.api_secret = api_secret

    def _create_signature(self, query_string):
        """Create HMAC SHA256 signature."""
        return hmac.new(
            self.api_secret.encode("utf-8"),
            query_string.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()

    def _get_headers(self):
        """Generate headers for the request."""
        return {"X-MBX-APIKEY": self.api_key}

    def _make_request(self, method, endpoint, params=None):
        """Make a signed request to the Binance API."""
        params = params or {}
        params["timestamp"] = int(time.time() * 1000)  # Add timestamp
        query_string = "&".join([f"{key}={value}" for key, value in params.items()])
        query_string += f"&signature={self._create_signature(query_string)}"

        url = f"{self.base_url}{endpoint}"
        headers = self._get_headers()

        if method == "GET":
            response = requests.get(url, headers=headers, params=params)
        elif method == "POST":
            response = requests.post(url, headers=headers, params=params)
        else:
            raise ValueError("Unsupported HTTP method.")

        response.raise_for_status()  # Raise an error for bad responses
        return response.json()

    def get_account_balance(self):
        """Fetch account balances with detailed debugging."""
        try:
            params = {"timestamp": int(time.time() * 1000)}
            query_string = "&".join([f"{key}={value}" for key, value in params.items()])
            signature = self._create_signature(query_string)
            query_string += f"&signature={signature}"

            url = f"{self.base_url}/v3/account?{query_string}"
            headers = self._get_headers()
            response = requests.get(url, headers=headers)

            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            print(f"HTTPError: {e}")
            print(f"Response Content: {response.text}")
            raise
        except Exception as e:
            print(f"Error: {e}")
            raise


    def place_market_order(self, symbol, side, quantity):
        """Place a market order."""
        params = {
            "symbol": symbol,
            "side": side,
            "type": "MARKET",
            "quantity": quantity,
        }
        return self._make_request("POST", "/v3/order", params)
