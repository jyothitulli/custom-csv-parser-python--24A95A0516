from custom_csv import SecureSheetReader, SecureSheetWriter
import os

def test_secure_roundtrip():
    # Data aligned with benchmark.py structure
    rows = [
        ["ID", "Name", "Plan", "Price", "Comment"],
        ["201", "Beta User", "Basic", "1000", "Simple test row"],
        ["305", 'Arjun "AJ" Singh', "Premium", "6000", 'Needs "full coverage"']
    ]

    test_file = "benchmark_verify.csv"

    # 1. Test Writing using your unique method
    with open(test_file, "w", encoding="utf-8", newline="") as f:
        exporter = SecureSheetWriter(f)
        exporter.add_bulk_rows(rows)

    # 2. Test Reading using your unique class
    read_rows = []
    with open(test_file, "r", encoding="utf-8") as f:
        engine = SecureSheetReader(f)
        for record in engine:
            read_rows.append(record)

    # 3. Assertions (Verifying your data matches perfectly)
    assert len(read_rows) == 3
    assert read_rows[0] == ["ID", "Name", "Plan", "Price", "Comment"]
    assert read_rows[1][1] == "Beta User"
    assert read_rows[2][1] == 'Arjun "AJ" Singh' # Checks complex quotes
    
    # Cleanup
    if os.path.exists(test_file):
        os.remove(test_file)