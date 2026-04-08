"""Generate cohort retention table."""

from datetime import timedelta, datetime
from backend.mock_data.generator import get_rng


def generate_retention_data() -> list[dict]:
    """Generate 8 weekly cohorts with retention percentages.

    More recent cohorts show a slight improvement trend.
    """
    rng = get_rng()
    now = datetime.now().date()
    cohorts: list[dict] = []

    for i in range(7, -1, -1):  # 8 cohorts, oldest first
        week_start = now - timedelta(weeks=i + 1)
        week_label = week_start.isoformat()

        # Improvement factor: newer cohorts retain slightly better
        improvement = 1.0 + (7 - i) * 0.012  # up to ~8% improvement

        initial_users = rng.randint(18_000, 25_000)

        # Base retention rates with noise
        day1 = round(min(rng.uniform(40, 48) * improvement, 58), 1)
        day3 = round(min(rng.uniform(28, 35) * improvement, 42), 1)
        day7 = round(min(rng.uniform(18, 24) * improvement, 30), 1)
        day14 = round(min(rng.uniform(12, 17) * improvement, 22), 1)
        day30 = round(min(rng.uniform(6, 10) * improvement, 14), 1)

        cohorts.append({
            "cohort_week": week_label,
            "initial_users": initial_users,
            "day1": day1,
            "day3": day3,
            "day7": day7,
            "day14": day14,
            "day30": day30,
        })

    return cohorts
