"""Generate 180 days of daily metrics."""

import math
from backend.mock_data.generator import get_rng, date_range

# Base values
_BASE_DAU = 128_000
_BASE_DEVICES = 95_000
_BASE_CASTS = 320_000
_BASE_REVENUE = 42_000.0
_BASE_NEW_USERS = 15_000
_BASE_SESSION_MIN = 25.0

TOTAL_DAYS = 180


def generate_daily_metrics() -> list[dict]:
    """Generate 180 days of daily metrics with realistic patterns."""
    rng = get_rng()
    dates = date_range(TOTAL_DAYS)
    data: list[dict] = []

    for idx, date in enumerate(dates):
        day_of_week = date.weekday()
        progress = idx / (TOTAL_DAYS - 1)  # 0 -> 1 over 180 days

        # Weekend boost for entertainment product
        weekend_factor = 1.25 if day_of_week >= 5 else 1.0

        # Growth trend: 1.0 -> 1.15
        trend = 1.0 + progress * 0.15

        # Weekly sine wave +/- 5%
        wave = math.sin(2 * math.pi * idx / 7) * 0.05

        # Random noise +/- 8%
        noise = rng.uniform(-0.08, 0.08)

        factor = trend * weekend_factor * (1 + wave + noise)

        dau = int(_BASE_DAU * factor)
        devices = int(_BASE_DEVICES * factor * rng.uniform(0.95, 1.05))
        casts = int(_BASE_CASTS * factor * rng.uniform(0.93, 1.07))
        revenue = round(_BASE_REVENUE * factor * rng.uniform(0.90, 1.10), 2)
        new_users = int(_BASE_NEW_USERS * factor * rng.uniform(0.90, 1.10))
        avg_session = round(_BASE_SESSION_MIN * (1 + (factor - 1) * 0.3) * rng.uniform(0.92, 1.08), 1)

        data.append({
            "date": date.isoformat(),
            "dau": dau,
            "active_devices": devices,
            "cast_count": casts,
            "revenue": revenue,
            "new_users": new_users,
            "avg_session_min": avg_session,
        })

    return data
