from web_socket_wrapper import BinanceWebSocket

async def stream_book_ticker(ws_url, symbol, data_manager):
    """Stream top-of-book data from Binance."""
    ws = BinanceWebSocket(ws_url, symbol)
    book_ticker_socket = await ws.connect_book_ticker()

    print("Connected to @bookTicker WebSocket")
    try:
        while True:
            data = await ws.receive_message(book_ticker_socket)
            print(f"@bookTicker data received")
            top_of_book = {
                "best_bid_price": float(data["b"]),
                "best_bid_qty": float(data["B"]),
                "best_ask_price": float(data["a"]),
                "best_ask_qty": float(data["A"]),
            }
            data_manager.update_top_of_book(top_of_book)
    except Exception as e:
        print(f"Error in stream_book_ticker: {e}")
    finally:
        await book_ticker_socket.close()
        print("@bookTicker WebSocket closed")


async def stream_depth(ws_url, symbol, data_manager):
    """Stream order book depth data from Binance."""
    ws = BinanceWebSocket(ws_url, symbol)
    depth_socket = await ws.connect_depth()

    print("Connected to @depth WebSocket")
    try:
        while True:
            data = await ws.receive_message(depth_socket)
            print(f"@depth data received")
            order_book_depth = {
                "bids": [[float(bid[0]), float(bid[1])] for bid in data["bids"]],
                "asks": [[float(ask[0]), float(ask[1])] for ask in data["asks"]],
            }
            data_manager.update_order_book_depth(order_book_depth)
    except Exception as e:
        print(f"Error in stream_depth: {e}")
    finally:
        await depth_socket.close()
        print("@depth WebSocket closed")
