from custom_csv.reader import CustomCsvReader

with CustomCsvReader("data.csv") as reader:
    for row in reader:
        print(row)
