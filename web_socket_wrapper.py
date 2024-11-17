import websockets
import json


class BinanceWebSocket:
    """WebSocket handler for Binance."""

    def __init__(self, ws_url, symbol):
        self.book_ticker_url = f"{ws_url}/{symbol}@bookTicker"
        self.depth_url = f"{ws_url}/{symbol}@depth20@100ms"

    async def connect_book_ticker(self):
        """Establish a WebSocket connection for @bookTicker."""
        return await websockets.connect(self.book_ticker_url)

    async def connect_depth(self):
        """Establish a WebSocket connection for @depth."""
        return await websockets.connect(self.depth_url)

    async def receive_message(self, websocket):
        """Receive a message from a WebSocket."""
        message = await websocket.recv()
        return json.loads(message)
