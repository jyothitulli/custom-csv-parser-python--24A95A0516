"""
Custom CSV Reader
Implements a streaming CSV parser with support for:
- comma-delimited fields
- quoted fields
- escaped quotes ("")
- embedded newlines inside quoted fields

Behavior is aligned with Python's csv.reader (permissive parsing).
"""

class CustomCsvReader:
    def __init__(self, file_path, delimiter=","):
        self.file_path = file_path
        self.delimiter = delimiter
        self.file = None

    def __enter__(self):
        self.file = open(self.file_path, "r", encoding="utf-8")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file:
            self.file.close()

    def __iter__(self):
        return self

    def __next__(self):
        field = ""
        row = []
        inside_quotes = False
        at_field_start = True

        while True:
            char = self.file.read(1)

            # EOF
            if not char:
                if field or row:
                    row.append(field)
                    return row
                raise StopIteration

            # Inside quoted field
            if inside_quotes:
                if char == '"':
                    next_char = self.file.read(1)
                    if next_char == '"':      # escaped quote
                        field += '"'
                    else:
                        inside_quotes = False
                        if next_char:
                            char = next_char
                        else:
                            continue
                else:
                    field += char
                continue

            # Start quoted field ONLY at field start
            if char == '"' and at_field_start:
                inside_quotes = True
                at_field_start = False
                continue

            # Field delimiter
            if char == self.delimiter:
                row.append(field)
                field = ""
                at_field_start = True
                continue

            # End of row
            if char == "\n":
                row.append(field)
                return row

            # Normal character (quotes included if unquoted)
            field += char
            at_field_start = False
