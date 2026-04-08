"""Mock data package -- pre-generates all data at import time.

Other modules should import data from here:
    from backend.mock_data import daily_data, hourly_data, ...
"""

from backend.mock_data.daily_metrics import generate_daily_metrics
from backend.mock_data.hourly_metrics import generate_hourly_metrics
from backend.mock_data.regional import generate_regional_data
from backend.mock_data.retention import generate_retention_data
from backend.mock_data.funnel import generate_funnel_data
from backend.mock_data.channels import generate_channel_data
from backend.mock_data.content import generate_top_content, generate_top_devices

# Pre-generate all datasets once (deterministic via shared seed)
daily_data: list[dict] = generate_daily_metrics()
hourly_data: list[dict] = generate_hourly_metrics()
regional_data: list[dict] = generate_regional_data()
retention_data: list[dict] = generate_retention_data()
funnel_data: list[dict] = generate_funnel_data()
channel_data: list[dict] = generate_channel_data()
top_content_data: list[dict] = generate_top_content()
top_devices_data: list[dict] = generate_top_devices()

__all__ = [
    "daily_data",
    "hourly_data",
    "regional_data",
    "retention_data",
    "funnel_data",
    "channel_data",
    "top_content_data",
    "top_devices_data",
]
