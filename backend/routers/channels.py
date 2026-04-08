"""Revenue channel breakdown endpoint."""

from fastapi import APIRouter, Query
from backend.mock_data import channel_data

router = APIRouter(prefix="/api")


@router.get("/channels")
async def get_channels(
    days: int = Query(default=7, ge=1, le=90),
):
    """Return daily revenue breakdown by channel for the last *days* days."""
    return {"channels": channel_data[-days:]}
