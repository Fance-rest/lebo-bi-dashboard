"""Retention cohort endpoint."""

from fastapi import APIRouter
from backend.mock_data import retention_data

router = APIRouter(prefix="/api")


@router.get("/retention")
async def get_retention():
    """Return cohort retention table."""
    return {"cohorts": retention_data}
