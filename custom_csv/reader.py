"""
Custom CSV Reader
Implements a streaming CSV parser with full support for:
- comma-delimited fields
- quoted fields
- escaped quotes ("")
- embedded newlines inside quotes
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
        """
        Reads and returns the next row as a list of fields.
        Implements a state machine for correct parsing.
        """
        field = ""
        row = []
        inside_quotes = False

        while True:
            char = self.file.read(1)

            # If EOF
            if not char:
                # Return last accumulated row if exists
                if field or row:
                    row.append(field)
                    return row
                raise StopIteration

            # If inside a quoted field
            if inside_quotes:
                # Escaped quote ("")
                if char == '"':
                    next_char = self.file.read(1)
                    if next_char == '"':  # escaped quote
                        field += '"'
                    else:
                        inside_quotes = False
                        if next_char:
                            # process the non-quote character normally
                            char = next_char
                        else:
                            continue
                else:
                    field += char
                continue

            # If char starts a quoted field
            if char == '"':
                inside_quotes = True
                continue

            # If comma → field ends
            if char == self.delimiter:
                row.append(field)
                field = ""
                continue

            # If newline → row ends
            if char == "\n":
                row.append(field)
                return row

            # Normal character
            field += char
