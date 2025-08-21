from fastapi import APIRouter, HTTPException
from polygon.rest.models import (
    TickerSnapshot,
)
from schwab.client import Client

from app.core.polygon_client import get_polygon_client
from app.core.schwab_client import get_schwab_client
from app.models.stock import (
    MoversFrequency,
    MoversIndex,
    MoversResponse,
    MoversSortOrder,
    PriceHistoryResponse,
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

        return PriceHistoryResponse(symbol=symbol.upper(), history=history)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching price history: {e!s}"
        ) from e


@router.get("/movers/schwab", response_model=MoversResponse)
async def get_stock_movers(
    index: MoversIndex, sort_order: MoversSortOrder, frequency: MoversFrequency
):
    """Get stock movers for a given index with specified sorting and frequency"""
    schwab_client = get_schwab_client()
    if not schwab_client:
        raise HTTPException(status_code=500, detail="Schwab client not initialized")

    try:
        print(
            f"Getting movers for index: {index}, sort_order: {sort_order}, frequency: {frequency}"
        )

        # Convert to Schwab client enums
        index_enum = getattr(Client.Movers.Index, index.name)
        sort_order_enum = getattr(Client.Movers.SortOrder, sort_order.name)
        frequency_enum = getattr(Client.Movers.Frequency, frequency.name)
        print(
            f"Index enum: {index_enum}, Sort order enum: {sort_order_enum}, Frequency enum: {frequency_enum}"
        )
        resp = schwab_client.get_movers(
            index_enum, sort_order=sort_order_enum, frequency=frequency_enum
        )
        print(f"Response: {resp.json()}")
        movers = resp.json().get("screeners")
        return MoversResponse(
            index=index, sort_order=sort_order, frequency=frequency, screeners=movers
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching stock movers: {e!s}"
        ) from e


@router.get("/movers")
async def get_top_market_movers(direction: str):
    """Get stock movers for a given direction"""
    polygon_client = get_polygon_client()
    if not polygon_client:
        raise HTTPException(status_code=500, detail="Polygon client not initialized")

    try:
        resp = polygon_client.get_snapshot_direction("stocks", direction=direction)
        movers = []
        for item in resp:
            if isinstance(item, TickerSnapshot):
                movers.append(
                    {
                        "symbol": item.ticker,
                        "todaysChange": item.todays_change,
                        "todaysChangePercent": item.todays_change_percent,
                        "previousClose": item.prev_day.close,
                        "volume": item.day.volume,
                        "minClose": item.min.close,
                    }
                )
        return movers
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching stock movers: {e!s}"
        ) from e
