from custom_csv.writer import CustomCsvWriter

def test_writer_basic(tmp_path):
    file_path = tmp_path / "output.csv"

    rows = [
        ["Name", "Message"],
        ["Alice", "Hello"],
        ["Bob", "Line1\nLine2"],
        ['He said "Hello"', "World"]
    ]

    with CustomCsvWriter(file_path) as writer:
        writer.write_rows(rows)

    content = file_path.read_text()

    expected = (
        'Name,Message\n'
        'Alice,Hello\n'
        '"Bob","Line1\nLine2"\n'
        '"He said ""Hello""",World\n'
    )

    assert content == expected
