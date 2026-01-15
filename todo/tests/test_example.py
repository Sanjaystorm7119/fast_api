def test_equal_or_not():
    assert 2 == 2
    assert 2 != 1

def test_isinstance():
    assert isinstance("hello", str)
    assert isinstance(10,int)

def test_is_bool():
    assert ("hello" == "world") is False

def test_is_type():
    assert type(10 is int)

def test_greater_than():
    assert 5 < 4

