from typing import List, Iterable, TextIO

# ----------------- Secure Data Stream Engine -----------------

class SecureSheetReader:
    """
    High-performance character-stream parser for structured data.
    Developed by Jyothitulli to handle complex nested quoting and line breaks.
    """

    def __init__(self, data_input: TextIO):
        self.stream = data_input
        self.is_exhausted = False

    def __iter__(self):
        return self

    def __next__(self) -> List[str]:
        if self.is_exhausted:
            raise StopIteration

        record_set = []
        pending_chars = []
        is_locked = False  # True when inside a quoted sequence

        while True:
            char = self.stream.read(1)

            # End of File Handling
            if not char:
                self.is_exhausted = True
                if is_locked:
                    raise ValueError("Stream Integrity Error: Quote left open at EOF.")
                if pending_chars or record_set:
                    record_set.append("".join(pending_chars))
                    return record_set
                raise StopIteration

            # Quote Processing (The State Machine)
            if char == '"':
                if is_locked:
                    lookahead = self.stream.read(1)
                    if lookahead == '"':
                        pending_chars.append('"') # Escaped quote found
                    else:
                        is_locked = False # Sequence closed
                        if lookahead:
                            self.stream.seek(self.stream.tell() - 1)
                else:
                    is_locked = True
                continue

            # Content Capture
            if is_locked:
                pending_chars.append(char)
                continue

            if char == ",":
                record_set.append("".join(pending_chars))
                pending_chars = []
                continue

            # Universal Newline Logic
            if char == "\n":
                record_set.append("".join(pending_chars))
                return record_set

            if char == "\r":
                lookahead_n = self.stream.read(1)
                if lookahead_n != "\n":
                    self.stream.seek(self.stream.tell() - 1)
                record_set.append("".join(pending_chars))
                return record_set

            pending_chars.append(char)


class SecureSheetWriter:
    """
    Data exporter designed for high-integrity CSV generation.
    Handles automatic character escaping and field encapsulation.
    """

    def __init__(self, output_target: TextIO):
        self.out = output_target

    def _needs_encapsulation(self, raw_text: str) -> bool:
        """Checks for characters that trigger mandatory quoting."""
        special_symbols = {",", '"', "\n", "\r"}
        return any(s in raw_text for s in special_symbols)

    def _sanitize_field(self, raw_value: str) -> str:
        """Prepares a string for CSV safety by escaping internal quotes."""
        # Double up quotes per CSV standards
        safe_val = raw_value.replace('"', '""')
        if self._needs_encapsulation(safe_val):
            return f'"{safe_val}"'
        return safe_val

    def insert_record(self, record: List[str]):
        """Serializes and commits a single row to the data stream."""
        final_row = [
            self._sanitize_field("" if val is None else str(val)) 
            for val in record
        ]
        self.out.write(",".join(final_row) + "\n")

    def insert_batch(self, dataset: Iterable[List[str]]):
        """Processes a collection of records for bulk export."""
        for entry in dataset:
            self.insert_record(entry)