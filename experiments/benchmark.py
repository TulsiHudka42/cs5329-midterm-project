
import argparse
import csv
import os
import sys
import time
import tracemalloc
import random

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "..", "src"))
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from utils import load_csv_records, comparable_records
from baseline import linear_search
from optimized import build_index, indexed_search

import matplotlib.pyplot as plt

RESULTS_CSV = os.path.join(os.path.dirname(CURRENT_DIR), "results", "benchmark_results.csv")
RESULTS_PNG = os.path.join(os.path.dirname(CURRENT_DIR), "results", "runtime_by_dataset.png")


def measure_linear(records, queries):
    tracemalloc.start()
    start = time.perf_counter()
    outputs = [linear_search(records, q) for q in queries]
    elapsed = time.perf_counter() - start
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return elapsed, peak, outputs


def measure_indexed(records, queries):
    tracemalloc.start()
    build_start = time.perf_counter()
    index = build_index(records)
    build_time = time.perf_counter() - build_start

    search_start = time.perf_counter()
    outputs = [indexed_search(index, q) for q in queries]
    search_time = time.perf_counter() - search_start
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return build_time, search_time, peak, outputs


def dataset_queries(records, query_count=200):
    random.seed(5329 + len(records))
    common = ["Shape of You", "Believer", "Levitating", "Blinding Lights", "Someone Like You"]
    unique_samples = []
    if records:
        unique_samples = [records[-1]["track_name"], records[len(records)//2]["track_name"]]
    base_queries = common + unique_samples + ["Definitely_Not_A_Song"]
    queries = [random.choice(base_queries) for _ in range(query_count)]
    return queries


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", nargs="+", required=True, help="One or more CSV dataset paths.")
    parser.add_argument("--query_count", type=int, default=200)
    args = parser.parse_args()

    os.makedirs(os.path.dirname(RESULTS_CSV), exist_ok=True)
    rows = []

    for dataset_path in args.dataset:
        records = load_csv_records(dataset_path)
        queries = dataset_queries(records, args.query_count)

        linear_time, linear_mem, linear_outputs = measure_linear(records, queries)
        build_time, indexed_search_time, indexed_mem, indexed_outputs = measure_indexed(records, queries)

        correctness = all(
            comparable_records(a) == comparable_records(b)
            for a, b in zip(linear_outputs, indexed_outputs)
        )

        rows.append(
            {
                "dataset": os.path.basename(dataset_path),
                "records": len(records),
                "queries": len(queries),
                "linear_total_seconds": linear_time,
                "linear_peak_bytes": linear_mem,
                "index_build_seconds": build_time,
                "indexed_search_seconds": indexed_search_time,
                "indexed_total_seconds": build_time + indexed_search_time,
                "indexed_peak_bytes": indexed_mem,
                "correctness_match": correctness,
            }
        )

    with open(RESULTS_CSV, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    sizes = [r["records"] for r in rows]
    linear_times = [r["linear_total_seconds"] for r in rows]
    indexed_total_times = [r["indexed_total_seconds"] for r in rows]
    indexed_lookup_only = [r["indexed_search_seconds"] for r in rows]

    plt.figure(figsize=(8, 5))
    plt.plot(sizes, linear_times, marker="o", label="Linear scan total")
    plt.plot(sizes, indexed_total_times, marker="o", label="Hash table total (build + queries)")
    plt.plot(sizes, indexed_lookup_only, marker="o", label="Hash table search only")
    plt.xlabel("Number of records")
    plt.ylabel("Time (seconds)")
    plt.title("Song Search Runtime Comparison")
    plt.legend()
    plt.tight_layout()
    plt.savefig(RESULTS_PNG, dpi=200)

    print(f"Saved benchmark results to {RESULTS_CSV}")
    print(f"Saved chart to {RESULTS_PNG}")
    for row in rows:
        print(row)


if __name__ == "__main__":
    main()
