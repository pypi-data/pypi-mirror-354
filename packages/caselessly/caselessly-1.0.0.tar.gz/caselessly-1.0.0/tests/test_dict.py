from caselessly import caselessdict, cidict


def test_caseless_dict_alias():
    assert caselessdict is cidict


def test_caseless_dict_instantiation():
    data = caselessdict()

    assert isinstance(data, caselessdict)
    assert isinstance(data, dict)

    assert len(data) == 0


def test_caseless_dict_instantiation_from_existing_dictionary():
    data = caselessdict({"a": 1, "B": 2})

    assert isinstance(data, caselessdict)
    assert isinstance(data, dict)

    assert len(data) == 2

    keys = list(data.keys())

    assert isinstance(keys, list)
    assert len(keys) == 2


def test_caseless_dict_instantiation_from_kwargs():
    data = caselessdict(a=1, B=2)

    assert isinstance(data, caselessdict)
    assert isinstance(data, dict)

    assert len(data) == 2


def test_caseless_dict_instantiation_from_existing_dictionary_and_kwargs():
    data = caselessdict({"a": 1, "B": 2}, c=3)

    assert isinstance(data, caselessdict)
    assert isinstance(data, dict)

    assert len(data) == 3

    assert data == {"A": 1, "B": 2, "c": 3}
    assert data == {"a": 1, "b": 2, "c": 3}
    assert data == {"a": 1, "B": 2, "c": 3}
    assert data == {"A": 1, "b": 2, "C": 3}


def test_caseless_dict():
    data = {
        "a": 1,
        "B": 2,
    }

    assert isinstance(data, dict)

    assert len(data) == 2

    assert data == {"a": 1, "B": 2}

    assert "a" in data
    assert not "A" in data
    assert "B" in data

    data = caselessdict(data)

    assert isinstance(data, caselessdict)
    assert isinstance(data, dict)

    assert len(data) == 2

    assert data == {"a": 1, "b": 2}

    assert "a" in data
    assert "A" in data

    assert data["a"] == 1
    assert data["A"] == 1

    assert "b" in data
    assert "B" in data

    assert data["B"] == 2
    assert data["b"] == 2

    assert data.keys() == ["a", "b"]
    assert data.keys() == ["A", "b"]
    assert data.keys() == ["a", "B"]
    assert data.keys() == ["A", "B"]

    data["C"] = 3

    assert "c" in data
    assert "C" in data

    assert data["c"] == 3
    assert data["C"] == 3

    assert data.keys() == ["a", "B", "C"]

    del data["B"]

    assert not "b" in data
    assert not "B" in data

    assert data.keys() == ["a", "C"]

    print(data.keys())
