"""CSV export endpoint."""

import csv
import io
from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse

from backend.mock_data import daily_data, regional_data, retention_data

router = APIRouter(prefix="/api")


def _to_csv(rows: list[dict]) -> str:
    """Convert a list of dicts to a CSV string."""
    if not rows:
        return ""
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)
    return output.getvalue()


@router.get("/export/csv")
async def export_csv(
    type: str = Query(default="metrics", pattern="^(metrics|regional|retention)$"),
    days: int = Query(default=30, ge=1, le=180),
):
    """Export data as a CSV file.

    type: metrics | regional | retention
    days: only applies to metrics
    """
    if type == "metrics":
        rows = daily_data[-days:]
        filename = f"metrics_{days}d.csv"
    elif type == "regional":
        rows = regional_data
        filename = "regional.csv"
    elif type == "retention":
        rows = retention_data
        filename = "retention.csv"
    else:
        rows = []
        filename = "export.csv"

    csv_content = _to_csv(rows)

    return StreamingResponse(
        iter([csv_content]),
        media_type="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename={filename}",
        },
    )
