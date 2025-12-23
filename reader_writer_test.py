from custom_csv import CustomCsvReader, CustomCsvWriter

rows = [
    ["PolicyID", "CustomerName", "PlanType", "Premium", "Notes"],
    ['104', 'Arjun "AJ" Singh', 'Health Premium', '6000', 'Needs "full coverage"'],
    ['105', 'Priya Sharma', 'Life Standard', '7800', 'Address updated']
]

with open("test.csv", "w", encoding="utf-8", newline="") as f:
    writer = CustomCsvWriter(f)
    writer.writerows(rows)

with open("test.csv", "r", encoding="utf-8") as f:
    reader = CustomCsvReader(f)
    for row in reader:
        print(row)