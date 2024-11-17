from binance.client import Client
from binance.enums import ORDER_TYPE_LIMIT, TIME_IN_FORCE_GTC, SIDE_BUY, SIDE_SELL

class OrderManager:
    def __init__(self, client: Client, pair: str):
        """
        Initialize the OrderManager.
        
        Args:
            client (Client): Binance API client.
            pair (str): The trading pair, e.g., 'BTCUSDT'.
        """
        self.client = client
        self.pair = pair
        self.active_orders = {}  # Track active orders by their IDs

    def place_order(self, side: str, price: float, order_size: float):
        """
        Place a limit order with a specified size.
        
        Args:
            side (str): 'BUY' or 'SELL'.
            price (float): The price at which to place the order.
            order_size (float): The size of the order.
        
        Returns:
            dict: The API response for the placed order.
        """
        try:
            order = self.client.create_order(
                symbol=self.pair,
                side=side,
                type=ORDER_TYPE_LIMIT,
                timeInForce=TIME_IN_FORCE_GTC,
                quantity=order_size,
                price=f"{price:.2f}",
            )
            self.active_orders[order["orderId"]] = order
            print(f"Placed {side} order at {price:.2f} for {order_size} {self.pair}")
            return order
        except Exception as e:
            print(f"Error placing {side} order at {price:.2f}: {e}")
            return None

    def cancel_order(self, order_id: str):
        """
        Cancel an active order.
        
        Args:
            order_id (str): The ID of the order to cancel.
        
        Returns:
            dict: The API response for the canceled order.
        """
        try:
            response = self.client.cancel_order(symbol=self.pair, orderId=order_id)
            if order_id in self.active_orders:
                del self.active_orders[order_id]
            print(f"Canceled order ID: {order_id}")
            return response
        except Exception as e:
            print(f"Error canceling order ID {order_id}: {e}")
            return None

    def cancel_all_orders(self):
        """
        Cancel all active orders for the trading pair.
        
        Returns:
            list: A list of responses for all canceled orders.
        """
        responses = []
        for order_id in list(self.active_orders.keys()):
            response = self.cancel_order(order_id)
            if response:
                responses.append(response)
        return responses

    def get_active_orders(self):
        """
        Retrieve the list of active orders from the API.
        
        Returns:
            list: A list of active orders.
        """
        try:
            active_orders = self.client.get_open_orders(symbol=self.pair)
            self.active_orders = {order["orderId"]: order for order in active_orders}
            return active_orders
        except Exception as e:
            print(f"Error fetching active orders: {e}")
            return []

    def get_position(self):
        """
        Retrieve the current position for the trading pair.
        
        Returns:
            dict: Position details (free and locked amounts).
        """
        try:
            account_info = self.client.get_account()
            balances = {asset["asset"]: asset for asset in account_info["balances"]}
            base_asset, quote_asset = self.pair[:-4], self.pair[-4:]
            return {
                "base": balances.get(base_asset, {"free": 0, "locked": 0}),
                "quote": balances.get(quote_asset, {"free": 0, "locked": 0}),
            }
        except Exception as e:
            print(f"Error fetching position: {e}")
            return {"base": {"free": 0, "locked": 0}, "quote": {"free": 0, "locked": 0}}
