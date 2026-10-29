import math
import re
from collections import Counter

STOPWORDS = frozenset(
    "a an and are as at be but by for from has have i if in into is it its my of on or "
    "so that the their then there these this to was were what when where which while who "
    "why will with you your how do does did not no can could should would".split()
)


def tokenize(text: str) -> list[str]:
    return [t for t in re.findall(r"[a-z0-9]+", text.lower()) if t not in STOPWORDS]

class BM25:
    def __init__(self, documents: list[str], k1: float = 1.5, b: float = 0.75):
        self.k1, self.b = k1, b
        tokens = [tokenize(doc) for doc in documents]
        self.doc_len = [len(t) for t in tokens]
        self.avg_len = sum(self.doc_len) / len(self.doc_len) if self.doc_len else 0.0
        self.term_freqs = [Counter(t) for t in tokens]

        document_frequency: Counter = Counter()
        for t in tokens:
            document_frequency.update(set(t))

        # inverse document frequency. it is a measure of how important a term is in the corpus. the more documents a term appears in, the less important it is. the less documents a term appears in, the more important it is. we use it to weight the term frequency in the bm25 formula.
        n = len(documents)
        self.idf = {term: math.log(1 + (n - df + 0.5) / (df + 0.5)) for term, df in document_frequency.items()}

    def scores(self, query: str) -> list[float]:
        terms = tokenize(query)
        result = []
        for freqs, length in zip(self.term_freqs, self.doc_len):
            score = 0.0
            for term in terms:
                tf = freqs.get(term)
                if not tf:
                    continue
                denom = tf + self.k1 * (1 - self.b + self.b * length / self.avg_len)
                score += self.idf[term] * tf * (self.k1 + 1) / denom

            result.append(score)

        return result
