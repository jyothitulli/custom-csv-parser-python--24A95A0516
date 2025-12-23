from typing import List, Iterable, TextIO


# ----------------- CSV Reader -----------------
class CustomCsvReader:
    """
    Streaming CSV reader implemented from scratch.
    Reads character-by-character without using Python's csv module.
    """

    def __init__(self, file: TextIO):
        self.file = file
        self.eof = False

    def __iter__(self):
        return self

    def __next__(self) -> List[str]:
        if self.eof:
            raise StopIteration

        row = []
        field = []
        in_quotes = False

        while True:
            ch = self.file.read(1)

            if ch == "":
                self.eof = True
                if in_quotes:
                    raise ValueError("Unexpected EOF inside quoted field")
                if field or row:
                    row.append("".join(field))
                    return row
                raise StopIteration

            if ch == '"':
                if in_quotes:
                    next_ch = self.file.read(1)
                    if next_ch == '"':
                        field.append('"')
                    else:
                        in_quotes = False
                        if next_ch:
                            self.file.seek(self.file.tell() - 1)
                else:
                    in_quotes = True
                continue

            if in_quotes:
                field.append(ch)
                continue

            if ch == ",":
                row.append("".join(field))
                field = []
                continue

            if ch == "\n":
                row.append("".join(field))
                return row

            if ch == "\r":
                next_ch = self.file.read(1)
                if next_ch != "\n":
                    self.file.seek(self.file.tell() - 1)
                row.append("".join(field))
                return row

            field.append(ch)


# ----------------- CSV Writer -----------------
class CustomCsvWriter:
    """Custom CSV writer implemented from scratch."""

    def __init__(self, file: TextIO):
        self.file = file

    def _needs_quotes(self, value: str) -> bool:
        return any(c in value for c in [",", '"', "\n", "\r"])

    def _format_field(self, value: str) -> str:
        value = value.replace('"', '""')
        if self._needs_quotes(value):
            return f'"{value}"'
        return value

    def writerow(self, row: List[str]):
        formatted = [self._format_field("" if v is None else str(v)) for v in row]
        self.file.write(",".join(formatted) + "\n")

    def writerows(self, rows: Iterable[List[str]]):
        for row in rows:
            self.writerow(row)