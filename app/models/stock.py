from enum import Enum
from typing import Any, Dict, List

from pydantic import BaseModel


# Enum classes for movers endpoint
class MoversIndex(str, Enum):
    DJI = "$DJI"
    COMPX = "$COMPX"
    SPX = "$SPX"
    NYSE = "NYSE"
    NASDAQ = "NASDAQ"
    OTCBB = "OTCBB"
    INDEX_ALL = "INDEX_ALL"
    EQUITY_ALL = "EQUITY_ALL"
    OPTION_ALL = "OPTION_ALL"
    OPTION_PUT = "OPTION_PUT"
    OPTION_CALL = "OPTION_CALL"


class MoversSortOrder(str, Enum):
    VOLUME = "VOLUME"
    TRADES = "TRADES"
    PERCENT_CHANGE_UP = "PERCENT_CHANGE_UP"
    PERCENT_CHANGE_DOWN = "PERCENT_CHANGE_DOWN"
    AVERAGE_PERCENT_VOLUME = "AVERAGE_PERCENT_VOLUME"


class MoversFrequency(int, Enum):
    ZERO = "0"
    ONE = "1"
    FIVE = "5"
    TEN = "10"
    THIRTY = "30"
    SIXTY = "60"


# Pydantic models for request/response
class StockSymbol(BaseModel):
    symbol: str


class PriceHistoryResponse(BaseModel):
    symbol: str
    history: Dict[str, Any]


class MoversResponse(BaseModel):
    index: MoversIndex
    sort_order: MoversSortOrder
    frequency: MoversFrequency
    screeners: List[Dict[str, Any]]
