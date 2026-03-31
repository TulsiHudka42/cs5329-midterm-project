# CS 5329 – Midterm Project

**Student Name:** Tulsi Mansukhbhai Hudka  
**Project Title:** Optimizing Large-Scale Song Search Using Hash Tables

## Overview
This project studies a simple but practical search problem: finding songs by title in a large Spotify-style dataset. I compared two approaches:

- **Baseline:** linear scan through every record
- **Optimized:** hash table lookup using a prebuilt index

The main goal was to see how algorithm choice affects runtime and memory usage as the dataset size grows.

## Problem Statement
The system takes a song title as input and returns matching song records from a large CSV dataset. The baseline approach checks records one by one, while the optimized approach preprocesses the dataset into a hash table so repeated searches can be answered much faster.

## Repository Structure
```text
cs5329-midterm-project/
├── README.md
├── report.md
├── requirements.txt
├── data/
│   ├── songs_10000.csv
│   ├── songs_50000.csv
│   └── songs_100000.csv
├── src/
│   ├── baseline.py
│   ├── optimized.py
│   └── utils.py
├── experiments/
│   ├── benchmark.py
│   └── generate_data.py
└── results/
    ├── benchmark_results.csv
    └── runtime_by_dataset.png
```

## How to Run

### 1. Install dependencies
```bash
pip3 install -r requirements.txt
```

### 2. Generate synthetic datasets
```bash
python3 experiments/generate_data.py --sizes 10000 50000 100000
```

This creates CSV files in `data/` named:
- `songs_10000.csv`
- `songs_50000.csv`
- `songs_100000.csv`

### 3. Run the benchmark
For one dataset:
```bash
python3 experiments/benchmark.py --dataset data/songs_10000.csv --query_count 200
```

For all three datasets:
```bash
python3 experiments/benchmark.py --dataset data/songs_10000.csv data/songs_50000.csv data/songs_100000.csv --query_count 200
```

### 4. Output
The benchmark script writes:
- `results/benchmark_results.csv`
- `results/runtime_by_dataset.png`

## Algorithms

### Baseline: Linear Scan
The program compares the query against every song title in the dataset until all matches are found.

- Time: **O(n)** per query
- Space: **O(k)** for matches

### Optimized: Hash Table
The dataset is first indexed using a Python dictionary where the normalized song title is the key and the value is a list of matching records.

- Build time: **O(n)**
- Lookup time: **O(1)** average per query
- Space: **O(n)**

## Evaluation Plan
- **Runtime:** measured with `time.perf_counter()`
- **Memory:** measured with `tracemalloc`
- **Correctness:** optimized results are compared against linear scan results
- **Dataset realism:** tested on multiple dataset sizes, repeated queries, existing titles, and missing titles

## Benchmark Results
I ran the benchmark with **200 queries** on three dataset sizes. The query set included common titles, unique titles, and one missing title.

| Dataset | Records | Queries | Linear Scan (s) | Hash Build (s) | Hash Search (s) | Hash Total (s) | Correctness |
|---|---:|---:|---:|---:|---:|---:|---|
| songs_10000.csv | 10,000 | 200 | 0.3301 | 0.0065 | 0.000053 | 0.0066 | True |
| songs_50000.csv | 50,000 | 200 | 1.6765 | 0.0220 | 0.000054 | 0.0220 | True |
| songs_100000.csv | 100,000 | 200 | 3.3457 | 0.0405 | 0.000052 | 0.0405 | True |

## Memory Results
| Dataset | Linear Peak Memory (bytes) | Hash Peak Memory (bytes) |
|---|---:|---:|
| songs_10000.csv | 61,294 | 1,555,610 |
| songs_50000.csv | 62,639 | 9,043,363 |
| songs_100000.csv | 63,682 | 18,087,378 |

## Summary of Findings
The results show the expected trade-off:
- **Linear scan** uses very little extra memory, but runtime increases quickly as the dataset grows.
- **Hash table lookup** requires extra memory and a preprocessing step, but it is much faster for repeated searches.
- The optimized approach returned the same results as the baseline in every benchmark, so the correctness check passed for all tested datasets.

