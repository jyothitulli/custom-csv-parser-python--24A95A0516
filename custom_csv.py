
from typing import List, Iterable, TextIO

# ----------------- Secure Data Stream Engine -----------------

class SecureSheetReader:
    """
    High-performance character-stream parser for structured data.
    Designed to handle complex nested quoting and line breaks.
    """

    def __init__(self, data_source: TextIO):
        self.source = data_source
        self.finished = False

    def __iter__(self):
        return self

    def __next__(self) -> List[str]:
        if self.finished:
            raise StopIteration

        current_record = []
        char_buffer = []
        is_protected = False  # Track if we are inside a quoted block

        while True:
            char = self.source.read(1)

            # Check for end of stream
            if char == "":
                self.finished = True
                if is_protected:
                    raise ValueError("Data Stream error: Unclosed quote at end of file.")
                if char_buffer or current_record:
                    current_record.append("".join(char_buffer))
                    return current_record
                raise StopIteration

            # Handle Quote Logic (State Machine)
            if char == '"':
                if is_protected:
                    peek = self.source.read(1)
                    if peek == '"':
                        char_buffer.append('"') # Found an escaped quote
                    else:
                        is_protected = False # Exiting quote block
                        if peek:
                            self.source.seek(self.source.tell() - 1)
                else:
                    is_protected = True
                continue

            # Capture characters if protected or not a delimiter
            if is_protected:
                char_buffer.append(char)
                continue

            if char == ",":
                current_record.append("".join(char_buffer))
                char_buffer = []
                continue

            # Handle Line Breaks (Windows and Unix)
            if char == "\n":
                current_record.append("".join(char_buffer))
                return current_record

            if char == "\r":
                peek_n = self.source.read(1)
                if peek_n != "\n":
                    self.source.seek(self.source.tell() - 1)
                current_record.append("".join(char_buffer))
                return current_record

            char_buffer.append(char)


class SecureSheetWriter:
    """
    Data exporter designed for high-integrity CSV generation.
    Handles automatic escaping for commas and quotes.
    """

    def __init__(self, target_dest: TextIO):
        self.destination = target_dest

    def _should_encapsulate(self, text: str) -> bool:
        """Determines if a string contains characters requiring quotes."""
        trigger_chars = [",", '"', "\n", "\r"]
        return any(sym in text for sym in trigger_chars)

    def _clean_and_wrap(self, content: str) -> str:
        """Escapes internal quotes and wraps field in double quotes if necessary."""
        # Standard CSV escape: Replace " with ""
        cleaned = content.replace('"', '""')
        if self._should_encapsulate(cleaned):
            return f'"{cleaned}"'
        return cleaned

    def add_row(self, data_row: List[str]):
        """Formats and writes a single list of data to the stream."""
        processed_fields = [
            self._clean_and_wrap("" if item is None else str(item)) 
            for item in data_row
        ]
        self.destination.write(",".join(processed_fields) + "\n")

    def add_bulk_rows(self, data_collection: Iterable[List[str]]):
        """Processes multiple rows sequentially."""
        for item in data_collection:
            self.add_row(item)