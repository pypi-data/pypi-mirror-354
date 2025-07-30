from caselessly import caselesstuple, cituple


def test_caseless_tuple_alias():
    assert caselesstuple is cituple


def test_caseless_tuple():
    data = tuple(["A", "B", "c", "D", "E", "f"])

    assert "A" in data
    assert "B" in data
    assert not "C" in data

    data = caselesstuple(data)

    assert "A" in data
    assert "B" in data
    assert "C" in data  # note that "C" does not exist in the list but "c" does
    assert "D" in data
    assert "E" in data
    assert "F" in data  # note that "F" does not exist in the list but "f" does
