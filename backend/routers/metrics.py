"""Metrics endpoints: daily summary and hourly breakdown."""

from fastapi import APIRouter, Query
from backend.mock_data import daily_data, hourly_data

router = APIRouter(prefix="/api")


@router.get("/metrics")
async def get_metrics(
    days: int = Query(default=7, ge=1, le=90),
    compare: bool = Query(default=False),
):
    """Return daily metrics for the most recent *days* days.

    If compare=True, also return the previous period and change percentages.
    """
    # Current period: last `days` rows from the 180-day dataset
    current = daily_data[-days:]

    latest = current[-1]
    summary = {
        "dau": latest["dau"],
        "active_devices": latest["active_devices"],
        "cast_count": sum(d["cast_count"] for d in current),
        "revenue": round(sum(d["revenue"] for d in current), 2),
        "new_users": sum(d["new_users"] for d in current),
        "avg_session_min": round(
            sum(d["avg_session_min"] for d in current) / len(current), 1
        ),
    }

    result: dict = {"summary": summary, "daily": current}

    if compare:
        previous = daily_data[-(2 * days) : -days]
        if previous:
            prev_summary = {
                "dau": previous[-1]["dau"],
                "active_devices": previous[-1]["active_devices"],
                "cast_count": sum(d["cast_count"] for d in previous),
                "revenue": round(sum(d["revenue"] for d in previous), 2),
                "new_users": sum(d["new_users"] for d in previous),
                "avg_session_min": round(
                    sum(d["avg_session_min"] for d in previous) / len(previous), 1
                ),
            }

            change_pct: dict = {}
            for key in ["dau", "active_devices", "cast_count", "revenue", "new_users", "avg_session_min"]:
                old_val = prev_summary[key]
                new_val = summary[key]
                if old_val:
                    change_pct[key] = round((new_val - old_val) / old_val * 100, 2)
                else:
                    change_pct[key] = 0.0

            summary["change_pct"] = change_pct
            result["previous"] = previous

    return result


@router.get("/metrics/hourly")
async def get_hourly_metrics(
    days: int = Query(default=7, ge=1, le=7),
):
    """Return hourly data for the specified number of recent days."""
    # hourly_data has 7 days * 24 hours = 168 rows
    rows_needed = days * 24
    return {"hourly": hourly_data[-rows_needed:]}
