import os
# Importing your unique classes
from custom_csv import SecureSheetReader, SecureSheetWriter

def test_secure_roundtrip():
    """
    Verifies the integrity of the SecureSheet engine using 
    data consistent with the project's benchmark suite.
    """
    # Data matches benchmark.py headers
    rows = [
        ["ID", "Name", "Plan", "Price", "Comment"],
        ["201", "Beta User", "Basic", "1000", "Simple test row"],
        ["305", 'Arjun "AJ" Singh', "Premium", "6000", 'Needs "full coverage"']
    ]

    test_temp_file = "verify_integrity.csv"

    # 1. Test Writing (using your new 'insert_batch' method)
    with open(test_temp_file, "w", encoding="utf-8", newline="") as f:
        exporter = SecureSheetWriter(f)
        exporter.insert_batch(rows)

    # 2. Test Reading (using your new 'SecureSheetReader' engine)
    read_results = []
    with open(test_temp_file, "r", encoding="utf-8") as f:
        engine = SecureSheetReader(f)
        for record in engine:
            read_results.append(record)

    # 3. Assertions (Validation logic)
    assert len(read_results) == 3
    assert read_results[0] == ["ID", "Name", "Plan", "Price", "Comment"]
    assert read_results[1][1] == "Beta User"
    
    # This specifically proves your state-machine handles quotes correctly
    assert read_results[2][1] == 'Arjun "AJ" Singh' 
    assert "full coverage" in read_results[2][4]
    
    # 4. Cleanup
    if os.path.exists(test_temp_file):
        os.remove(test_temp_file)