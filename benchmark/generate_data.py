"""
Generate synthetic CSV data for benchmarking.
Creates a CSV file with 10,000 rows and 5 columns.

Fields may contain:
- commas
- quotes
- newlines

Output is RFC 4180–compliant.
"""

import random
import string


def random_text():
    base = ''.join(random.choices(string.ascii_letters, k=8))
    choice = random.randint(1, 5)

    if choice == 1:
        return base + ",extra"           # contains comma
    elif choice == 2:
        return 'He said "Hello"'         # contains quotes
    elif choice == 3:
        return "Line1\nLine2"            # contains newline
    else:
        return base


def escape_field(field: str) -> str:
    """
    RFC 4180–compliant CSV escaping:
    - Fields containing comma, quote, or newline are quoted
    - Quotes inside fields are escaped as ""
    """
    if any(c in field for c in [',', '"', '\n']):
        field = field.replace('"', '""')
        return f'"{field}"'
    return field


def generate_csv(file_path, rows=10000, cols=5):
    with open(file_path, "w", encoding="utf-8", newline="") as f:
        for _ in range(rows):
            row = [escape_field(random_text()) for _ in range(cols)]
            f.write(",".join(row) + "\n")


if __name__ == "__main__":
    print("Generating dataset...")
    generate_csv("benchmark_data.csv")
    print("Done.")
