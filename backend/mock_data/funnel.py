"""Generate casting funnel data."""

from backend.mock_data.generator import get_rng

_STAGES = [
    ("app_open", "应用打开", 1.00),
    ("device_discovery", "设备发现", 0.72),
    ("connection_start", "开始连接", 0.58),
    ("cast_success", "投屏成功", 0.45),
    ("content_play", "内容播放", 0.38),
]

_BASE_COUNT = 1_000_000


def generate_funnel_data() -> list[dict]:
    """Generate a 5-stage casting funnel with counts and conversion rates."""
    rng = get_rng()
    data: list[dict] = []
    prev_count = None

    for stage_id, label, target_rate in _STAGES:
        noise = rng.uniform(0.96, 1.04)
        count = int(_BASE_COUNT * target_rate * noise)

        if prev_count is None:
            rate = 100.0
        else:
            rate = round(count / prev_count * 100, 1)

        overall_rate = round(count / (_BASE_COUNT * _STAGES[0][2] * 1.0) * 100, 1)

        data.append({
            "stage": stage_id,
            "label": label,
            "count": count,
            "rate_from_prev": rate,
            "rate_from_start": overall_rate,
        })

        prev_count = count

    return data
