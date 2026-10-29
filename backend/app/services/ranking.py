from dataclasses import dataclass

# data class means that this class is mainly used to store data and automatically generates special methods like __init__(), __repr__(), and __eq__() for convenience. The frozen=True parameter makes instances of the class immutable, meaning their attributes cannot be changed after they are created.
# kw_only=True means that all the fields in the dataclass must be specified as keyword arguments when creating an instance of the class. This can help improve code readability and prevent errors that may arise from positional arguments.
@dataclass(frozen=True, kw_only=True)
class Hit:
    note_id: int
    chunk_index: int
    score: float   # score of the hit, higher is better
    content: str
    title: str = ""

def top_notes(hits: list[Hit], k: int) -> list[Hit]:
    """Keep each note's best chunk, then return the k best notes."""
    best: dict[int, Hit] = {}
    for hit in hits:
        current = best.get(hit.note_id)
        if current is None or hit.score > current.score:
            best[hit.note_id] = hit
    ranked = sorted(best.values(), key=lambda h: (-h.score, h.note_id, h.chunk_index))
    return ranked[:k]