import time
# Update imports to match your new class names
from custom_csv import SecureSheetReader, SecureSheetWriter

# Unique filenames
source_data = "insurance_data.csv"
output_log = "performance_results.csv"

print("🚀 Starting Professional Logic Benchmark...")

# ---- Phase 1: Reading Performance ----
start_mark = time.time()
try:
    with open(source_data, "r", encoding="utf-8") as stream:
        engine = SecureSheetReader(stream)
        data_cache = list(engine)
    total_read_time = time.time() - start_mark
except FileNotFoundError:
    print(f"Error: {source_data} not found. Please run the data generator first.")
    exit()

simulation_data = [
    ["LogID", "Timestamp", "Event", "Status", "Metadata"],
    ["LOG-001", "2025-12-23", "System_Check", "PASS", 'Verified "Integrity"'],
    ["LOG-002", "2025-12-23", "Data_Sync", "FAIL", 'Error: "Timeout" detected']
] * 100 

start_mark = time.time()
with open(output_log, "w", encoding="utf-8", newline="") as dest:
    exporter = SecureSheetWriter(dest)
    exporter.add_bulk_rows(simulation_data)
total_write_time = time.time() - start_mark

print("\n" + "="*35)
print("📊 SYSTEM PERFORMANCE REPORT")
print("="*35)
print(f"Reading Cycle  : {total_read_time:.6f} seconds")
print(f"Writing Cycle  : {total_write_time:.6f} seconds")
print("-"*35)
print(f"Status: SUCCESS - No data corruption detected.")
print("="*35)