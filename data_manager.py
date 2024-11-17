class DataManager:
    def __init__(self):
        self.top_of_book = {}
        self.order_book_depth = {}
        self.listeners = []

    def register_listener(self, listener):
        """Register a new listener for updates."""
        self.listeners.append(listener)

    def unregister_listener(self, listener):
        """Unregister a listener."""
        self.listeners.remove(listener)

    def update_top_of_book(self, top_of_book):
        self.top_of_book = top_of_book
        print(f"Top-of-book updated")  # Debug
        self.broadcast_update()

    def update_order_book_depth(self, order_book_depth):
        self.order_book_depth = order_book_depth
        print(f"Order book depth updated")  # Debug
        self.broadcast_update()

    def broadcast_update(self):
        """Broadcast updates to all registered listeners."""
        for listener in self.listeners:
            listener(self.top_of_book, self.order_book_depth)
