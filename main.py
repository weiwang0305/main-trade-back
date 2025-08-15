from typing import Union
from fastapi import FastAPI
from dotenv import load_dotenv
import os
from schwab.auth import easy_client
from schwab.client import Client
from schwab.streaming import StreamClient
import ssl

import asyncio
import json

load_dotenv()

print("Initializing Schwab client...")
print("If this is your first time, a browser will open for authentication.")

try:
    c = easy_client(
      api_key=os.getenv('SCHWAB_APP_KEY'),
      app_secret=os.getenv('SCHWAB_APP_SECRET'),
      callback_url=os.getenv('SCHWAB_CALLBACK_URL'),
      token_path='tmp/token.json'
    )
    
    print("Getting price history for AAPL...")
    resp = c.get_price_history_every_day('AAPL')
    history = resp.json()
    # print(history)
    
except Exception as e:
    print(f"Error: {e}")
    print("Make sure your .env file has the correct SCHWAB_APP_KEY, SCHWAB_APP_SECRET, and SCHWAB_CALLBACK_URL values.")


account_number_resp = c.get_account_numbers()
account_hash = account_number_resp.json()[0]['hashValue']


ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

stream_client = StreamClient(c, account_id=account_hash, ssl_context=ssl_context)


async def read_stream():
  await stream_client.login()
  
  def print_message(msg):
    print(json.dumps(msg, indent=2))
  
  stream_client.add_nasdaq_book_handler(print_message)
  await stream_client.nasdaq_book_subs(['AAPL'])

  while True:
    await stream_client.handle_message()

asyncio.run(read_stream())




