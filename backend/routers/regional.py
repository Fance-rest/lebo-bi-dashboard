"""Regional data endpoint."""

from fastapi import APIRouter
from backend.mock_data import regional_data

router = APIRouter(prefix="/api")


@router.get("/regional")
async def get_regional():
    """Return per-province metrics."""
    return {"provinces": regional_data}
