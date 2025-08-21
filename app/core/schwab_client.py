import ssl

from schwab.auth import easy_client
from schwab.streaming import StreamClient

from app.core.config import settings

# Global variables for Schwab client
schwab_client = None
account_hash = None
stream_client = None
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE


def initialize_schwab_client():
    """Initialize the Schwab client"""
    global schwab_client, account_hash

    try:
        print("Initializing Schwab client...")
        print("If this is your first time, a browser will open for authentication.")

        schwab_client = easy_client(
            api_key=settings.SCHWAB_APP_KEY,
            app_secret=settings.SCHWAB_APP_SECRET,
            callback_url=settings.SCHWAB_CALLBACK_URL,
            token_path=settings.TOKEN_PATH,
        )

        # Get account information
        account_number_resp = schwab_client.get_account_numbers()
        account_hash = account_number_resp.json()[0]["hashValue"]

        print("Schwab client initialized successfully!")
        return True

    except Exception as e:
        print(f"Error initializing Schwab client: {e}")
        print(
            "Make sure your .env file has the correct SCHWAB_APP_KEY, SCHWAB_APP_SECRET, and SCHWAB_CALLBACK_URL values."
        )
        return False


async def initialize_stream_client():
    global stream_client, account_hash, schwab_client
    try:
        print("Initializing Schwab stream client...")
        stream_client = StreamClient(
            schwab_client, account_id=account_hash, ssl_context=ssl_context
        )
        await stream_client.login()
        print("Schwab stream client initialized successfully!")
        return True
    except Exception as e:
        print(f"Error initializing Schwab stream client: {e}")
        return False


def get_schwab_client():
    """Get the initialized Schwab client"""
    return schwab_client


def get_stream_client():
    """Get the initialized Schwab stream client"""
    return stream_client


def get_account_hash():
    """Get the account hash"""
    return account_hash


async def create_request_stream_client():
    """Create a new stream client for a specific request"""
    if not schwab_client:
        raise Exception("Schwab client not initialized")

    account_hash = get_account_hash()
    if not account_hash:
        raise Exception("Account hash not available")

    # Create SSL context for this request
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    # Create and login to a new stream client
    request_stream_client = StreamClient(
        schwab_client, account_id=account_hash, ssl_context=ssl_context
    )
    await request_stream_client.login()

    return request_stream_client
