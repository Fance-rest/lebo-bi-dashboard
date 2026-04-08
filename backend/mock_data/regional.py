"""Generate per-province regional data for ECharts map."""

from backend.mock_data.generator import get_rng

# Provinces ordered roughly by economic size / internet penetration
_PROVINCES = [
    ("广东省", 440000, 1.00),
    ("江苏省", 320000, 0.82),
    ("浙江省", 330000, 0.78),
    ("山东省", 370000, 0.72),
    ("河南省", 410000, 0.65),
    ("四川省", 510000, 0.60),
    ("湖北省", 420000, 0.52),
    ("湖南省", 430000, 0.50),
    ("河北省", 130000, 0.48),
    ("福建省", 350000, 0.46),
    ("安徽省", 340000, 0.42),
    ("北京市", 110000, 0.40),
    ("上海市", 310000, 0.38),
    ("辽宁省", 210000, 0.35),
    ("陕西省", 610000, 0.32),
    ("重庆市", 500000, 0.30),
    ("江西省", 360000, 0.28),
    ("广西壮族自治区", 450000, 0.26),
    ("云南省", 530000, 0.24),
    ("天津市", 120000, 0.22),
    ("山西省", 140000, 0.20),
    ("贵州省", 520000, 0.18),
    ("吉林省", 220000, 0.16),
    ("黑龙江省", 230000, 0.15),
    ("内蒙古自治区", 150000, 0.13),
    ("新疆维吾尔自治区", 650000, 0.11),
    ("甘肃省", 620000, 0.10),
    ("海南省", 460000, 0.08),
    ("宁夏回族自治区", 640000, 0.06),
    ("青海省", 630000, 0.05),
    ("西藏自治区", 540000, 0.03),
]

_BASE_USERS = 150_000
_BASE_CASTS = 400_000
_BASE_REVENUE = 50_000.0


def generate_regional_data() -> list[dict]:
    """Generate per-province metrics."""
    rng = get_rng()
    data: list[dict] = []

    for name, adcode, weight in _PROVINCES:
        noise = rng.uniform(0.88, 1.12)
        users = int(_BASE_USERS * weight * noise)
        casts = int(_BASE_CASTS * weight * rng.uniform(0.85, 1.15))
        revenue = round(_BASE_REVENUE * weight * rng.uniform(0.85, 1.15), 2)

        data.append({
            "name": name,
            "adcode": adcode,
            "active_users": users,
            "cast_count": casts,
            "revenue": revenue,
        })

    return data
