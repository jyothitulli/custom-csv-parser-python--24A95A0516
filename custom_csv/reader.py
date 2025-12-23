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

            if inside_quotes:
                if char == '"':
                    next_char = self.file.read(1)
                    if next_char == '"':  # escaped quote
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

            # Start of quoted field ONLY if at field start
            if char == '"' and at_field_start:
                inside_quotes = True
                at_field_start = False
                continue

            # Escaped quote inside UNQUOTED field
            if char == '"':
                next_char = self.file.read(1)
                if next_char == '"':
                    field += '"'
                    at_field_start = False
                    continue
                else:
                    field += '"'
                    if next_char:
                        field += next_char
                    at_field_start = False
                    continue

            if char == self.delimiter:
                row.append(field)
                field = ""
                at_field_start = True
                continue

            if char == "\n":
                row.append(field)
                return row

            field += char
            at_field_start = False
