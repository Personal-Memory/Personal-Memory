import random

def hit_at_k(ranked_note_ids: list[int], target: int, k: int) -> int:
    return int(target in ranked_note_ids[:k])

def reciprocal_rank(ranked_note_ids: list[int], target: int, k: int) -> float:
    for position, note_id in enumerate(ranked_note_ids[:k], start=1):
        if note_id == target:
            return 1 / position
    return 0.0

def mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0
 
def bootstrap_ci(values: list[float], iterations: int = 2000, seed: int = 0) -> tuple[float, float]:
    """95% confidence interval for the mean, by resampling."""
    if not values:
        return (0.0, 0.0)

    rng = random.Random(seed)
    n = len(values)
    means = sorted(mean([values[rng.randrange(n)] for _ in range(n)]) for _ in range(iterations))
    return (means[int(0.025 * iterations)], means[int(0.975 * iterations) - 1])