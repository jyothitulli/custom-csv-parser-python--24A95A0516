from custom_csv import CustomCsvReader, CustomCsvWriter
import os

def test_csv_roundtrip():
    rows = [
        ["PolicyID", "CustomerName", "PlanType", "Premium", "Notes"],
        ['104', 'Arjun "AJ" Singh', 'Health Premium', '6000', 'Needs "full coverage"'],
        ['105', 'Priya Sharma', 'Life Standard', '7800', 'Address updated']
    ]

    # Test Writing
    with open("test.csv", "w", encoding="utf-8", newline="") as f:
        writer = CustomCsvWriter(f)
        writer.writerows(rows)

    # Test Reading
    read_rows = []
    with open("test.csv", "r", encoding="utf-8") as f:
        reader = CustomCsvReader(f)
        for row in reader:
            read_rows.append(row)

    # Assertions (This is what pytest looks for!)
    assert len(read_rows) == 3
    assert read_rows[0] == ["PolicyID", "CustomerName", "PlanType", "Premium", "Notes"]
    assert read_rows[1][1] == 'Arjun "AJ" Singh'
    
    # Cleanup
    if os.path.exists("test.csv"):
        os.remove("test.csv")