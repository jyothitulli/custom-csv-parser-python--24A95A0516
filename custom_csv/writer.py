"""
Custom CSV Writer
Builds well-formed CSV files with:
- automatic quoting of fields containing comma, quote, or newline
- escaping internal quotes by doubling ("")
"""

class CustomCsvWriter:
    def __init__(self, file_path, delimiter=","):
        self.file_path = file_path
        self.delimiter = delimiter

    def __enter__(self):
        self.file = open(self.file_path, "w", encoding="utf-8", newline="")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file:
            self.file.close()

    def _escape_field(self, field: str) -> str:
        """
        Escape quotes and wrap field in quotes if necessary.
        """
        needs_quotes = (
            ',' in field or
            '"' in field or
            '\n' in field or
            '\r' in field
        )

        if '"' in field:
            field = field.replace('"', '""')  # escape internal quotes

        if needs_quotes:
            field = f'"{field}"'

        return field

    def write_row(self, row):
        escaped_fields = [self._escape_field(str(col)) for col in row]
        line = self.delimiter.join(escaped_fields)
        self.file.write(line + "\n")

    def write_rows(self, rows):
        for row in rows:
            self.write_row(row)
