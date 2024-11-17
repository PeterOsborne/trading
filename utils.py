# utils.py
def format_price(price, precision=6):
    """Format price to show a fixed number of decimal places."""
    return f"{price:.{precision}f}"
