"""Core random generator with fixed seed for reproducible mock data."""

import random
import math
from datetime import datetime, timedelta

from backend.config import DATA_SEED

_rng = random.Random(DATA_SEED)


def get_rng() -> random.Random:
    """Return the shared seeded Random instance."""
    return _rng


def rand_int(lo: int, hi: int) -> int:
    """Return a random integer in [lo, hi]."""
    return _rng.randint(lo, hi)


def rand_float(lo: float, hi: float) -> float:
    """Return a random float in [lo, hi]."""
    return _rng.uniform(lo, hi)


def today() -> datetime:
    """Return today's date as a datetime (date portion only)."""
    return datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)


def date_range(days: int) -> list:
    """Return a list of date objects for the past *days* days ending today."""
    t = datetime.now().date()
    return [t - timedelta(days=i) for i in range(days - 1, -1, -1)]
