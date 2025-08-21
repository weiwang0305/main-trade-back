from fastapi import APIRouter

from app.core.schwab_client import get_schwab_client

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/")
async def health_check():
    """Basic health check endpoint"""
    return {"status": "healthy"}


@router.get("/streams")
async def stream_health_check():
    """Check the status of streaming connections"""
    schwab_client = get_schwab_client()

    return {
        "status": "healthy" if schwab_client else "unhealthy",
        "schwab_client_initialized": schwab_client is not None,
    }
