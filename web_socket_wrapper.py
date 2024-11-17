import websockets
import json


class BinanceWebSocket:
    """WebSocket handler for Binance."""

    def __init__(self, ws_url, symbol):
        self.ws_url = ws_url
        self.symbol = symbol

    async def connect(self):
        """Establish a WebSocket connection."""
        url = f"{self.ws_url}/{self.symbol}@depth5"
        return await websockets.connect(url)

    async def receive_order_book(self, websocket):
        """Receive order book data from WebSocket."""
        message = await websocket.recv()
        return json.loads(message)
