from custom_csv.reader import read_csv

def test_simple_csv(tmp_path):
    file = tmp_path / "test.csv"
    file.write_text("a,b,c\n1,2,3")

    result = read_csv(file)
    assert result == [["a","b","c"],["1","2","3"]]

def test_quoted_fields(tmp_path):
    file = tmp_path / "test.csv"
    file.write_text('"a,b",c\n"1,2",3')

    result = read_csv(file)
    assert result == [["a,b","c"],["1,2","3"]]
