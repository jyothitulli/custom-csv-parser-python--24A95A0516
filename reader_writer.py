from custom_csv import SecureSheetReader, SecureSheetWriter
import os

def test_secure_roundtrip():
    # Unique data: E-commerce Order Logs (to differentiate from others)
    rows = [
        ["OrderID", "Customer", "ItemDescription", "Total", "ShippingNotes"],
        ['ORD-99', 'Sarah "The Boss" Miller', 'Ultra-Wide Monitor', '450.00', 'Fragile; "handle with care"'],
        ['ORD-100', 'Tech Corp, Inc.', 'Keyboard (Mechanical)', '120.50', 'Leave at "Rear Entrance"']
    ]

    # Test Writing using your new add_bulk_rows method
    with open("test_verify.csv", "w", encoding="utf-8", newline="") as f:
        exporter = SecureSheetWriter(f)
        exporter.add_bulk_rows(rows)

    # Test Reading using your new SecureSheetReader
    read_rows = []
    with open("test_verify.csv", "r", encoding="utf-8") as f:
        engine = SecureSheetReader(f)
        for record in engine:
            read_rows.append(record)

    # Assertions updated to match your new data
    assert len(read_rows) == 3
    assert read_rows[0] == ["OrderID", "Customer", "ItemDescription", "Total", "ShippingNotes"]
    assert read_rows[1][1] == 'Sarah "The Boss" Miller'
    assert "handle with care" in read_rows[1][4]
    
    # Cleanup
    if os.path.exists("test_verify.csv"):
        os.remove("test_verify.csv")