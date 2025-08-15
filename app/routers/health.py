from fastapi import APIRouter
from app.core.schwab_client import get_schwab_client

router = APIRouter(tags=["health"])

@router.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Schwab Trading API is running!", "status": "healthy"}

@router.get("/health")
async def health_check():
    """Detailed health check"""
    schwab_client = get_schwab_client()
    
    health_status = {
        "status": "healthy",
        "schwab_client_initialized": schwab_client is not None,
        "timestamp": "2024-01-01T00:00:00Z"  # You can add proper timestamp here
    }
    
    if not schwab_client:
        health_status["status"] = "degraded"
        health_status["message"] = "Schwab client not initialized"
    
    return health_status

@router.get("/ready")
async def readiness_check():
    """Readiness check for the application"""
    schwab_client = get_schwab_client()
    
    if not schwab_client:
        return {"status": "not_ready", "message": "Schwab client not initialized"}
    
    return {"status": "ready", "message": "Application is ready to serve requests"}
