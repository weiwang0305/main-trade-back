from typing import Union, Dict, Any
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from schwab.auth import easy_client
from schwab.client import Client
from schwab.streaming import StreamClient
import ssl
import asyncio
import json
from contextlib import asynccontextmanager

# Load environment variables
load_dotenv()



# Global variables for Schwab client
schwab_client = None
account_hash = None

# Pydantic models for request/response
class StockSymbol(BaseModel):
    symbol: str

class PriceHistoryResponse(BaseModel):
    symbol: str
    history: Dict[str, Any]

# Initialize Schwab client
def initialize_schwab_client():
    global schwab_client, account_hash
    
    try:
        print("Initializing Schwab client...")
        print("If this is your first time, a browser will open for authentication.")
        
        schwab_client = easy_client(
            api_key=os.getenv('SCHWAB_APP_KEY'),
            app_secret=os.getenv('SCHWAB_APP_SECRET'),
            callback_url=os.getenv('SCHWAB_CALLBACK_URL'),
            token_path='tmp/token.json'
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




# Initialize client on startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_schwab_client()
    yield


# Initialize FastAPI app
app = FastAPI(
    title="Schwab Trading API",
    description="A FastAPI application for Schwab trading operations",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Basic health check endpoint
@app.get("/")
async def root():
    return {"message": "Schwab Trading API is running!", "status": "healthy"}

# Get stock price history
@app.get("/stock/{symbol}/history", response_model=PriceHistoryResponse)
async def get_stock_history(symbol: str):
    if not schwab_client:
        raise HTTPException(status_code=500, detail="Schwab client not initialized")
    
    try:
        resp = schwab_client.get_price_history_every_day(symbol.upper())
        history = resp.json()
        
        return PriceHistoryResponse(
            symbol=symbol.upper(),
            history=history
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching price history: {str(e)}")

# Get account information
@app.get("/account")
async def get_account_info():
    if not schwab_client:
        raise HTTPException(status_code=500, detail="Schwab client not initialized")
    
    try:
        account_info = schwab_client.get_account_numbers()
        return {"accounts": account_info.json()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching account info: {str(e)}")

# Streaming endpoint (placeholder for future implementation)
@app.get("/stream/{symbol}")
async def start_streaming(symbol: str):
    return {"message": f"Streaming endpoint for {symbol} - Not implemented yet"}

# Error handling
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return {"error": str(exc), "status": "error"}

