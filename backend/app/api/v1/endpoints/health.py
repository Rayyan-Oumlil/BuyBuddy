from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health():
    """Health check endpoint."""
    return {
        "status": "ok",
        "message": "BuyBuddy API is running"
    }

