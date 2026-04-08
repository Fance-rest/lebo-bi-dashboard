"""Generate revenue channel breakdown data."""

import math
from backend.mock_data.generator import get_rng, date_range

_CHANNELS = [
    ("VIP会员", 0.35),
    ("广告收入", 0.28),
    ("内容分成", 0.18),
    ("增值服务", 0.12),
    ("硬件合作", 0.07),
]

_BASE_DAILY_REVENUE = 42_000.0
CHANNEL_DAYS = 90


def generate_channel_data() -> list[dict]:
    """Generate 90 days of daily revenue broken down by channel."""
    rng = get_rng()
    dates = date_range(CHANNEL_DAYS)
    data: list[dict] = []

    for idx, date in enumerate(dates):
        progress = idx / (CHANNEL_DAYS - 1)
        trend = 1.0 + progress * 0.12
        weekend_factor = 1.15 if date.weekday() >= 5 else 1.0
        daily_total = _BASE_DAILY_REVENUE * trend * weekend_factor

        row: dict = {"date": date.isoformat()}

        for channel_name, proportion in _CHANNELS:
            noise = rng.uniform(0.88, 1.12)
            amount = round(daily_total * proportion * noise, 2)
            row[channel_name] = amount

        data.append(row)

    return data
