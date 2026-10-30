import json
from pathlib import Path

import numpy as np

from app.services.chunking import chunk_index_text, chunk_text
from evaluation.bm25 import BM25

from app.services.ranking import Hit, top_notes
from evaluation.metrics import hit_at_k, reciprocal_rank

from evaluation.metrics import bootstrap_ci, mean

import argparse
import datetime

from app.services.embeddings import (
    DEFAULT_GEMINI_MODEL, EMBEDDING_DIM, EmbeddingError, GeminiEmbedder, HashingEmbedder,
)
from evaluation.cache import CachedEmbedder

DATASET_PATH = Path(__file__).parent / "dataset.json"

def ranked_note_ids(scores, note_ids, k=5, min_score=None):
    """One score per chunk -> the top-k note ids (best chunk per note)."""
    hits = [
        Hit(note_id=note_id, chunk_index=i, score=float(s), content="")
        for i, (s, note_id) in enumerate(zip(scores, note_ids))
        if min_score is None or float(s) > min_score
    ]
    return [h.note_id for h in top_notes(hits, k)]


def score(ranked_lists, targets, k=5):
    """Per-query results, kept per query so the CI and paired table are possible."""
    return {
        "hits": [float(hit_at_k(r, t, k)) for r, t in zip(ranked_lists, targets)],
        "rrs": [reciprocal_rank(r, t, k) for r, t in zip(ranked_lists, targets)],
    }


def paired(vec_hits, bm25_hits):
    buckets = {"both": [], "vector_only": [], "bm25_only": [], "neither": []}
    for i, (v, b) in enumerate(zip(vec_hits, bm25_hits)):
        if v and b:
            buckets["both"].append(i)
        elif v:
            buckets["vector_only"].append(i)
        elif b:
            buckets["bm25_only"].append(i)
        else:
            buckets["neither"].append(i)
    return buckets


def load_dataset(path=DATASET_PATH):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def build_corpus(notes, max_chars=600, overlap_chars=100):
    """Return (chunk_texts, chunk_note_ids): one entry per chunk, title included."""
    texts, note_ids = [], []
    for note in notes:
        for chunk in chunk_text(note["text"], max_chars, overlap_chars):
            texts.append(chunk_index_text(note["title"], chunk))
            note_ids.append(note["id"])
    return texts, note_ids


def vector_rankings(embedder, chunk_texts, chunk_note_ids, queries, k=5):
    doc_vecs = np.array(embedder.embed_documents(chunk_texts), dtype=float)
    query_vecs = np.array(embedder.embed_queries(queries), dtype=float)
    sims = query_vecs @ doc_vecs.T  # vectors are L2-normalised, so this is cosine
    return [ranked_note_ids(row, chunk_note_ids, k) for row in sims]


def bm25_rankings(chunk_texts, chunk_note_ids, queries, k=5):
    bm25 = BM25(chunk_texts)
    return [ranked_note_ids(bm25.scores(q), chunk_note_ids, k, min_score=0.0) for q in queries]

def summarize(scores_dict, query_types):
    """Recall@5, MRR@5 and 95% bootstrap CIs for all / paraphrase / keyword queries."""
    out = {}
    for label in ("all", "paraphrase", "keyword"):
        idx = [i for i, t in enumerate(query_types) if label == "all" or t == label]
        hits = [scores_dict["hits"][i] for i in idx]
        rrs = [scores_dict["rrs"][i] for i in idx]
        out[label] = {
            "n": len(idx),
            "recall": mean(hits),
            "recall_ci": bootstrap_ci(hits),
            "mrr": mean(rrs),
            "mrr_ci": bootstrap_ci(rrs),
        }
    return out


CACHE_DIR = Path(__file__).parent / ".cache"
SWEEP_SIZES = (200, 350, 600)


def overlap_for(size):
    return min(100, size // 4)


def make_embedder(name):
    if name == "hashing":
        inner, namespace = HashingEmbedder(), f"hashing-{EMBEDDING_DIM}"
    elif name == "gemini":
        inner, namespace = GeminiEmbedder(), f"{DEFAULT_GEMINI_MODEL}-{EMBEDDING_DIM}"
    else:
        raise ValueError(f"unknown embedder: {name!r}")
    return CachedEmbedder(inner, CACHE_DIR / f"{name}.json", namespace)


def run_config(embedder, data, max_chars, overlap_chars, k=5):
    texts, note_ids = build_corpus(data["notes"], max_chars, overlap_chars)
    queries = [q["q"] for q in data["queries"]]
    targets = [q["note"] for q in data["queries"]]
    types = [q["type"] for q in data["queries"]]

    vec_ranked = vector_rankings(embedder, texts, note_ids, queries, k)
    bm_ranked = bm25_rankings(texts, note_ids, queries, k)
    vec, bm = score(vec_ranked, targets, k), score(bm_ranked, targets, k)
    return {
        "config": {"max_chars": max_chars, "overlap_chars": overlap_chars, "k": k,
                   "chunks": len(texts), "notes": len(data["notes"]), "queries": len(queries)},
        "vector": summarize(vec, types),
        "bm25": summarize(bm, types),
        "paired": paired(vec["hits"], bm["hits"]),
        "ranked": {"vector": vec_ranked, "bm25": bm_ranked},
    }


def print_report(result):
    c = result["config"]
    print(f"\n== chunk size {c['max_chars']} (overlap {c['overlap_chars']}): "
          f"{c['chunks']} chunks, {c['queries']} queries ==")
    for label in ("all", "paraphrase", "keyword"):
        for method in ("vector", "bm25"):
            r = result[method][label]
            print(f"{label:<11}{method:<7}n={r['n']:<4}"
                  f"Recall@5 {r['recall']:.3f} [{r['recall_ci'][0]:.3f}, {r['recall_ci'][1]:.3f}]  "
                  f"MRR@5 {r['mrr']:.3f} [{r['mrr_ci'][0]:.3f}, {r['mrr_ci'][1]:.3f}]")
    print("paired:", {name: len(idx) for name, idx in result["paired"].items()})


def print_failures(result, data):
    for bucket in ("neither", "bm25_only", "vector_only"):
        print(f"\n-- {bucket} --")
        for i in result["paired"][bucket]:
            q = data["queries"][i]
            print(f"[{q['type']}] {q['q']!r}  expected={q['note']}  "
                  f"vector={result['ranked']['vector'][i]}  bm25={result['ranked']['bm25'][i]}")


def main(argv=None):
    parser = argparse.ArgumentParser(description="Evaluate retrieval on the synthetic dataset.")
    parser.add_argument("--embedder", choices=["gemini", "hashing"], default="gemini")
    parser.add_argument("--sweep", action="store_true", help="try chunk sizes 200/350/600")
    parser.add_argument("--show-failures", action="store_true")
    parser.add_argument("--out", help="write results to this JSON file")
    args = parser.parse_args(argv)

    data = load_dataset()
    embedder = make_embedder(args.embedder)
    sizes = SWEEP_SIZES if args.sweep else (600,)
    runs = []
    try:
        for size in sizes:
            result = run_config(embedder, data, size, overlap_for(size))
            print_report(result)
            if args.show_failures:
                print_failures(result, data)
            runs.append(result)
    except EmbeddingError as error:
        print(f"\nEmbedding failed ({error}). Progress is cached; rerun to continue.")
        return 1

    print(f"\nTexts embedded through the API this run: {embedder.new_texts}")
    if args.out:
        for run in runs:
            run.pop("ranked")  # keep the JSON small
        payload = {"date": datetime.date.today().isoformat(), "embedder": args.embedder,
                   "model": embedder.namespace, "runs": runs}
        Path(args.out).write_text(json.dumps(payload, indent=2), encoding="utf-8")
        print(f"Wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())