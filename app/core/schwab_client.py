from schwab.auth import easy_client
from schwab.client import Client
from app.core.config import settings

# Global variables for Schwab client
schwab_client = None
account_hash = None

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
            token_path=settings.TOKEN_PATH
        )
        
        # Get account information
        account_number_resp = schwab_client.get_account_numbers()
        account_hash = account_number_resp.json()[0]['hashValue']
        
        print("Schwab client initialized successfully!")
        return True
        
    except Exception as e:
        print(f"Error initializing Schwab client: {e}")
        print("Make sure your .env file has the correct SCHWAB_APP_KEY, SCHWAB_APP_SECRET, and SCHWAB_CALLBACK_URL values.")
        return False

def get_schwab_client():
    """Get the initialized Schwab client"""
    return schwab_client

def get_account_hash():
    """Get the account hash"""
    return account_hash
