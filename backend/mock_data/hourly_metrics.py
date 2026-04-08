"""Generate hourly metrics for the last 7 days."""

from datetime import timedelta, datetime
from backend.mock_data.generator import get_rng

# Hourly activity pattern (0-23) -- relative weights
_HOURLY_PATTERN_WEEKDAY = [
    0.10, 0.06, 0.04, 0.03, 0.03, 0.05,  # 0-5: very low
    0.12, 0.25, 0.55, 0.60, 0.45, 0.40,  # 6-11: morning ramp
    0.58, 0.50, 0.42, 0.40, 0.45, 0.55,  # 12-17: afternoon
    0.70, 0.90, 1.00, 0.95, 0.75, 0.40,  # 18-23: evening prime
]

_HOURLY_PATTERN_WEEKEND = [
    0.15, 0.10, 0.06, 0.04, 0.04, 0.06,  # 0-5: low but slightly higher
    0.12, 0.20, 0.35, 0.50, 0.60, 0.65,  # 6-11: slower morning
    0.70, 0.65, 0.60, 0.58, 0.60, 0.65,  # 12-17: flat afternoon
    0.75, 0.92, 1.00, 0.95, 0.80, 0.50,  # 18-23: evening prime
]

_BASE_ACTIVE = 90_000
_BASE_CASTS = 12_000


def generate_hourly_metrics(days: int = 7) -> list[dict]:
    """Generate hour-by-hour metrics for the specified number of days."""
    rng = get_rng()
    now = datetime.now().date()
    data: list[dict] = []

    for d in range(days - 1, -1, -1):
        date = now - timedelta(days=d)
        is_weekend = date.weekday() >= 5
        pattern = _HOURLY_PATTERN_WEEKEND if is_weekend else _HOURLY_PATTERN_WEEKDAY
        overall_boost = 1.15 if is_weekend else 1.0

        for hour in range(24):
            weight = pattern[hour]
            noise = rng.uniform(0.90, 1.10)
            active = int(_BASE_ACTIVE * weight * overall_boost * noise)
            casts = int(_BASE_CASTS * weight * overall_boost * rng.uniform(0.88, 1.12))

            data.append({
                "day": date.isoformat(),
                "hour": hour,
                "active_users": active,
                "cast_count": casts,
            })

    return data
