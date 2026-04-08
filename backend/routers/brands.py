"""Brand distribution endpoint."""

from fastapi import APIRouter
from backend.mock_data.generator import get_rng

router = APIRouter(prefix="/api")


def _generate_brand_distribution() -> list[dict]:
    """Generate device brand market-share distribution."""
    rng = get_rng()
    brands = [
        {"name": "小米", "value": rng.randint(30, 38)},
        {"name": "海信", "value": rng.randint(18, 25)},
        {"name": "TCL", "value": rng.randint(14, 20)},
        {"name": "华为", "value": rng.randint(8, 12)},
        {"name": "创维", "value": rng.randint(5, 9)},
    ]
    total = sum(b["value"] for b in brands)
    brands.append({"name": "其他", "value": 100 - total})
    return brands


# Pre-generate so it stays consistent
_brand_data = _generate_brand_distribution()


@router.get("/brands")
async def get_brands():
    """Return device brand distribution."""
    return {"brands": _brand_data}
