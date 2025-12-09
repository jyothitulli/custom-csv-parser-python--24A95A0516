# custom-csv-parser-python--24A95A0516
A custom CSV reader and writer implemented from scratch in Python with benchmarking against the built-in csv module.
# Custom CSV Parser in Python

A complete implementation of a **CSV Reader** and **CSV Writer** built from scratch in Python—without using Python's built-in `csv` module.

This project demonstrates low-level parsing, handling malformed CSVs, escaping, quoting, embedded newlines, and benchmarking.

---

# 🚀 Features

### ✔ Custom CSV Reader
- Comma-delimited parsing  
- Handles:
  - Fields enclosed in quotes
  - Escaped quotes ("")
  - Newlines inside quoted fields
- Streaming parser (does NOT load file into memory)
- Implemented as a Python iterator (`__iter__`, `__next__`)

### ✔ Custom CSV Writer
- Automatically quotes fields containing:
  - commas
  - quotes
  - newlines
- Escapes quotes inside fields
- Efficient row writing

### ✔ Benchmarking
- Compares:
  - CustomCsvReader vs `csv.reader`
  - CustomCsvWriter vs `csv.writer`
- Uses synthetic data (10,000 rows)

---

# 📂 Project Structure
custom-csv-parser-python/
│
├── custom_csv/
│ ├── reader.py
│ ├── writer.py
│
├── benchmark/
│ ├── generate_data.py
│ ├── benchmark_reader_writer.py
│
├── requirements.txt
└── README.md

# 🛠 Setup Instructions

### 1. Clone the repository
```bash
git clone < https://github.com/jyothitulli/custom-csv-parser-python--24A95A0516>
cd custom-csv-parser-python--24A95A0516

Reading a CSV
from custom_csv.reader import CustomCsvReader

with CustomCsvReader("data.csv") as reader:
    for row in reader:
        print(row)

Writing a CSV
from custom_csv.writer import CustomCsvWriter

rows = [
    ["Hello", "World"],
    ["He said \"Hello\"", "Line1\nLine2"]
]

with CustomCsvWriter("output.csv") as writer:
    writer.write_rows(rows)

Generate dataset
python benchmark/generate_data.py

Run benchmark
python benchmark/benchmark_reader_writer.py

#example output
--- Reader Benchmark ---
Custom Reader: 0.78 seconds
Stdlib Reader: 0.07 seconds

--- Writer Benchmark ---
Custom Writer: 0.59 seconds
Stdlib Writer: 0.11 seconds

Benchmark Analysis

The Python built-in csv module is implemented in optimized C code, so it performs significantly faster than the custom Python implementation.
Our custom reader and writer handle all required CSV edge cases correctly but naturally run slower because every character is parsed manually in Python.
The benchmark demonstrates the trade-off between control and transparency (custom implementation) vs speed and optimization (stdlib module).
This confirms that the custom parser works properly and meets all functional requirements, though not as fast as the highly optimized standard library.

#git commands

git add .
git commit -m "Complete custom CSV parser project"
git push origin main
