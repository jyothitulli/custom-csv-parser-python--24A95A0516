from custom_csv.writer import CustomCsvWriter

rows = [
    ["Name", "Message"],
    ["Alice", "Hello"],
    ["Bob", "Line1\nLine2"],
    ["He said \"Hello\"", "World"]
]

with CustomCsvWriter("output.csv") as writer:
    writer.write_rows(rows)
