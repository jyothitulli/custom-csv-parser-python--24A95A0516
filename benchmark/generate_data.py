"""
Generate synthetic CSV data for benchmarking.
Creates a CSV file with 10,000 rows and 5 columns.
Some fields include commas, quotes, and newlines.
"""

import random
import string

def random_text():
    base = ''.join(random.choices(string.ascii_letters, k=8))
    choice = random.randint(1, 5)

    if choice == 1:
        return base + ",extra"
    elif choice == 2:
        return 'He said "Hello"'
    elif choice == 3:
        return "Line1\nLine2"
    else:
        return base

def generate_csv(file_path, rows=10000, cols=5):
    with open(file_path, "w", encoding="utf-8", newline="") as f:
        for _ in range(rows):
            row = [random_text() for _ in range(cols)]
            f.write(",".join([r.replace('"', '""') if '"' in r else r for r in row]) + "\n")

if __name__ == "__main__":
    print("Generating dataset...")
    generate_csv("benchmark_data.csv")
    print("Done.")
