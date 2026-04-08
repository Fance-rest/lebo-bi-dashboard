"""Casting funnel endpoint."""

from fastapi import APIRouter
from backend.mock_data import funnel_data

router = APIRouter(prefix="/api")


@router.get("/funnel")
async def get_funnel():
    """Return casting funnel stages."""
    return {"stages": funnel_data}
