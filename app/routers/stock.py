from fastapi import APIRouter, HTTPException
from schwab.client import Client
from app.core.schwab_client import get_schwab_client
from app.models.stock import (
    PriceHistoryResponse, 
    MoversResponse, 
    MoversIndex, 
    MoversSortOrder, 
    MoversFrequency
)

router = APIRouter(prefix="/stock", tags=["stock"])

@router.get("/{symbol}/history", response_model=PriceHistoryResponse)
async def get_stock_history(symbol: str):
    """Get stock price history for a given symbol"""
    schwab_client = get_schwab_client()
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

@router.get("/movers", response_model=MoversResponse)
async def get_stock_movers(
    index: MoversIndex, 
    sort_order: MoversSortOrder, 
    frequency: MoversFrequency
):
    """Get stock movers for a given index with specified sorting and frequency"""
    schwab_client = get_schwab_client()
    if not schwab_client:
        raise HTTPException(status_code=500, detail="Schwab client not initialized")
    
    try:
        print(f"Getting movers for index: {index}, sort_order: {sort_order}, frequency: {frequency}")
        
        # Convert to Schwab client enums
        index_enum = getattr(Client.Movers.Index, index.name)
        sort_order_enum = getattr(Client.Movers.SortOrder, sort_order.name)
        frequency_enum = getattr(Client.Movers.Frequency, frequency.name)
        
        resp = schwab_client.get_movers(index_enum, sort_order=sort_order_enum, frequency=frequency_enum)
        movers = resp.json().get('screeners')
        return MoversResponse(index=index, sort_order=sort_order, frequency=frequency, screeners=movers)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching stock movers: {str(e)}")

