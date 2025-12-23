from custom_csv import SecureSheetReader

def load_records(file_path):
    with open("insurance_data.csv", "r", encoding="utf-8") as f:
        reader = SecureSheetReader(f)
        rows = list(reader)

    headers = rows[0]
    return [dict(zip(headers, row)) for row in rows[1:]]

def main():
    records = load_records("insurance_data.csv")

    print("---- SEARCH MODE ----")
    while True:
        query = input("Ask your question (or 'exit'): ").strip().lower()
        if query == "exit":
            break

        results = []
        for row in records:
            if query in " ".join(row.values()).lower():
                results.append(row)

        if not results:
            print("No results found.\n")
            continue

        for r in results:
            print(r)
        print()

if __name__ == "__main__":
    main()