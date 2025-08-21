from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.alpaca_client import initialize_alpaca_client
from app.core.config import settings
from app.core.polygon_client import initialize_polygon_client
from app.core.schwab_client import initialize_schwab_client, initialize_stream_client
from app.routers import account, health, stock


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """Application lifespan manager"""
    initialize_schwab_client()
    await initialize_stream_client()
    initialize_alpaca_client()
    initialize_polygon_client()
    yield


# Initialize FastAPI app
app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION,
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router)
app.include_router(stock.router)
app.include_router(account.router)


# Error handling
@app.exception_handler(Exception)
async def global_exception_handler(_request, exc):
    return {"error": str(exc), "status": "error"}
