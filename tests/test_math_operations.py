from math_operations import add

def test_add_positive_numbers():
    assert add(1, 2) == 3
    assert add(5, 5) == 10

def test_add_negative_numbers():
    assert add(-1, -2) == -3
    assert add(-5, 5) == 0

def test_add_zero():
    assert add(0, 0) == 0
    assert add(5, 0) == 5
    assert add(0, 5) == 5 
