"""
Benchmark custom reader/writer vs Python's csv module.
"""

import csv
import timeit
from custom_csv.reader import CustomCsvReader
from custom_csv.writer import CustomCsvWriter

DATA_FILE = "benchmark_data.csv"
OUT_FILE_CUSTOM = "output_custom.csv"
OUT_FILE_STDLIB = "output_stdlib.csv"


def benchmark_custom_reader():
    def run():
        with CustomCsvReader(DATA_FILE) as reader:
            for row in reader:
                pass
    return timeit.timeit(run, number=5)


def benchmark_std_reader():
    def run():
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            for row in csv.reader(f):
                pass
    return timeit.timeit(run, number=5)


def benchmark_custom_writer():
    def run():
        rows = []
        with CustomCsvReader(DATA_FILE) as reader:
            for r in reader:
                rows.append(r)
        with CustomCsvWriter(OUT_FILE_CUSTOM) as writer:
            writer.write_rows(rows)
    return timeit.timeit(run, number=3)


def benchmark_std_writer():
    def run():
        rows = []
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            for r in csv.reader(f):
                rows.append(r)
        with open(OUT_FILE_STDLIB, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            for r in rows:
                w.writerow(r)
    return timeit.timeit(run, number=3)


if __name__ == "__main__":
    print("Running benchmark...")

    print("\n--- Reader Benchmark ---")
    print("Custom Reader:", benchmark_custom_reader(), "seconds")
    print("Stdlib Reader:", benchmark_std_reader(), "seconds")

    print("\n--- Writer Benchmark ---")
    print("Custom Writer:", benchmark_custom_writer(), "seconds")
    print("Stdlib Writer:", benchmark_std_writer(), "seconds")
