import re
from typing import Any

# After each of these block types we emit a newline, so paragraphs/list items stay separate.
BLOCK_TYPES = {"paragraph", "heading", "listItem", "taskItem", "blockquote", "codeBlock"}

def extract_text(document: Any) -> str:
    parts: list[str] = []

    def walk(node: Any) -> None:
        if not isinstance(node, dict):
            return
        node_type = node.get("type")
        if node_type == "text":
            parts.append(node.get("text", ""))      # no separator: marks split words
        elif node_type == "hardBreak":
            parts.append("\n")
        for child in node.get("content") or []:
            walk(child)
        if node_type in BLOCK_TYPES:
            parts.append("\n") 

    walk(document)
    lines = [re.sub(r"[ \t]+", " ", line).strip() for line in "".join(parts).split("\n")]
    return "\n".join(line for line in lines if line)

DEFAULT_MAX_CHARS = 600
DEFAULT_OVERLAP_CHARS = 100
_SENTENCE_END = re.compile(r"(?<=[.!?])\s+")   # split after . ! ? followed by whitespace


def _split_long(unit: str, max_chars: int) -> list[str]:
    """A single 'sentence' longer than max_chars (no punctuation): split on words."""
    pieces, current = [], ""
    for word in unit.split():
        while len(word) > max_chars:             # one giant token, e.g. a pasted URL
            if current:
                pieces.append(current)
                current = ""
            pieces.append(word[:max_chars])
            word = word[max_chars:]
        if not current:
            current = word
        elif len(current) + 1 + len(word) <= max_chars:
            current += " " + word
        else:
            pieces.append(current)
            current = word
    if current:
        pieces.append(current)
    return pieces


def _units(text: str, max_chars: int) -> list[str]:
    units: list[str] = []
    for line in text.split("\n"):
        for sentence in _SENTENCE_END.split(line.strip()):
            sentence = sentence.strip()
            if not sentence:
                continue
            units.extend(_split_long(sentence, max_chars) if len(sentence) > max_chars else [sentence])
    return units


def chunk_text(text: str, max_chars: int = DEFAULT_MAX_CHARS,
               overlap_chars: int = DEFAULT_OVERLAP_CHARS) -> list[str]:
    if max_chars <= 0:
        raise ValueError("max_chars must be positive")
    if not 0 <= overlap_chars < max_chars:
        raise ValueError("overlap_chars must be >= 0 and < max_chars")

    chunks: list[str] = []
    current: list[str] = []
    current_len = 0

    for unit in _units(text.strip(), max_chars):
        added = len(unit) + (1 if current else 0)
        if current and current_len + added > max_chars:
            chunks.append(" ".join(current))
            # carry trailing sentences (up to overlap_chars) into the next chunk
            carry, carry_len = [], 0
            for previous in reversed(current):
                extra = len(previous) + (1 if carry else 0)
                if carry_len + extra > overlap_chars:
                    break
                carry.insert(0, previous)
                carry_len += extra
            current, current_len = carry, carry_len
            added = len(unit) + (1 if current else 0)
            if current and current_len + added > max_chars:   # overlap doesn't fit: drop it
                current, current_len, added = [], 0, len(unit)
        current.append(unit)
        current_len += added

    if current:
        chunks.append(" ".join(current))
    return chunks

def chunk_index_text(title: str, chunk: str) -> str:
    title = title.strip()
    return f"{title}\n{chunk}" if title else chunk