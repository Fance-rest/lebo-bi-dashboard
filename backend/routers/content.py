"""Top content and top device endpoints."""

from fastapi import APIRouter, Query
from backend.mock_data import top_content_data, top_devices_data

router = APIRouter(prefix="/api")


@router.get("/content/top")
async def get_top_content(
    limit: int = Query(default=10, ge=1, le=50),
):
    """Return top cast content."""
    return {"content": top_content_data[:limit]}


@router.get("/devices/top")
async def get_top_devices(
    limit: int = Query(default=10, ge=1, le=50),
):
    """Return top active device models."""
    return {"devices": top_devices_data[:limit]}
