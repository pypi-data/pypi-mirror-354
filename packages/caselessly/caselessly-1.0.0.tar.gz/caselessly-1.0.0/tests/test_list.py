from caselessly import caselesslist, cilist


def test_caseless_list_alias():
    assert caselesslist is cilist


def test_caseless_list():
    data = ["A", "B", "c", "D", "E", "f"]

    assert isinstance(data, list)
    assert len(data) == 6

    assert "A" in data
    assert "B" in data
    assert not "C" in data

    data = caselesslist(data)

    assert isinstance(data, list)
    assert isinstance(data, caselesslist)
    assert len(data) == 6

    assert "A" in data
    assert "B" in data
    assert "C" in data  # note that "C" does not exist in the list but "c" does
    assert "D" in data
    assert "E" in data
    assert "F" in data  # note that "F" does not exist in the list but "f" does
