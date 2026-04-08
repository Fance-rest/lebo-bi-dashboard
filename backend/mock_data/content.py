"""Generate top content and top device data."""

from backend.mock_data.generator import get_rng

_TOP_CONTENT = [
    ("庆余年第二季", "电视剧"),
    ("热辣滚烫", "电影"),
    ("歌手2024", "综艺"),
    ("繁花", "电视剧"),
    ("飞驰人生2", "电影"),
    ("王者荣耀S35", "游戏"),
    ("英雄联盟S14", "直播"),
    ("奔跑吧第八季", "综艺"),
    ("三体第二季", "电视剧"),
    ("第二十条", "电影"),
]

_TOP_DEVICES = [
    ("小米", "Xiaomi TV Max 86\""),
    ("海信", "Hisense U7K 75\""),
    ("TCL", "TCL C845 65\""),
    ("华为", "Huawei Vision S3 Pro"),
    ("创维", "Skyworth A5D Pro 75\""),
    ("小米", "Xiaomi TV S Pro 65\""),
    ("海信", "Hisense E8K 65\""),
    ("TCL", "TCL Q10H 85\""),
    ("华为", "Huawei Vision SE3 55\""),
    ("创维", "Skyworth G5 65\""),
]


def generate_top_content() -> list[dict]:
    """Generate top 10 most-cast content items."""
    rng = get_rng()
    base_count = 850_000
    data: list[dict] = []

    for idx, (name, category) in enumerate(_TOP_CONTENT):
        decay = 0.82 ** idx  # each rank drops ~18%
        noise = rng.uniform(0.90, 1.10)
        count = int(base_count * decay * noise)
        data.append({
            "rank": idx + 1,
            "name": name,
            "category": category,
            "cast_count": count,
        })

    return data


def generate_top_devices() -> list[dict]:
    """Generate top 10 most-active device models."""
    rng = get_rng()
    base_count = 120_000
    data: list[dict] = []

    for idx, (brand, model) in enumerate(_TOP_DEVICES):
        decay = 0.80 ** idx  # each rank drops ~20%
        noise = rng.uniform(0.88, 1.12)
        count = int(base_count * decay * noise)
        data.append({
            "rank": idx + 1,
            "brand": brand,
            "model": model,
            "active_count": count,
        })

    return data
