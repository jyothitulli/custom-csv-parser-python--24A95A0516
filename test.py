import os
from custom_csv import SecureSheetReader

def start_search_tool():
    # We use the output from benchmark.py as our data source
    data_source = "benchmark_output.csv"
    
    if not os.path.exists(data_source):
        print(f" Error: '{data_source}' not found.")
        print("Please run 'python benchmark.py' first to generate the data!")
        return

    print("--- SecureSheet Search Tool ---")
    
    records = []
    with open(data_source, "r", encoding="utf-8") as stream:
        engine = SecureSheetReader(stream)
        # Load all rows into memory for searching
        for row in engine:
            records.append(row)

    if not records:
        print("The data file is empty.")
        return

    # Use the first row as headers
    headers = records[0]
    data_rows = records[1:]

    while True:
        query = input("\nEnter search term (or 'exit' to quit): ").strip().lower()
        if query == 'exit':
            break

        found = False
        for row in data_rows:
            # Check if query exists in any column of the row
            if any(query in str(field).lower() for field in row):
                # Format the output nicely
                result = dict(zip(headers, row))
                print(f"Match Found: {result}")
                found = True
        
        if not found:
            print(f"No results found for '{query}'.")

if __name__ == "__main__":
    start_search_tool()