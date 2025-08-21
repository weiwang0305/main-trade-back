from alpaca.data.live import CryptoDataStream, StockDataStream

from app.core.config import Settings

crypto_stream = None
stock_stream = None


def initialize_alpaca_client():
    """Initialize the Alpaca client"""
    global crypto_stream, stock_stream
    print("Initializing Alpaca client...")
    crypto_stream = CryptoDataStream(
        Settings.ALPACA_API_KEY, Settings.ALPACA_SECRET_KEY
    )
    stock_stream = StockDataStream(Settings.ALPACA_API_KEY, Settings.ALPACA_SECRET_KEY)
    print("Alpaca client initialized successfully!")


def get_crypto_stream():
    return crypto_stream


def get_stock_stream():
    return stock_stream
