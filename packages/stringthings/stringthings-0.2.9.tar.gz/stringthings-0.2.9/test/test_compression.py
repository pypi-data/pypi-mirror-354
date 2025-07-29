from stringthings import expand, compress

test_string_1 = '0 1 2 3 4 5 6 7 8 9'
test_string_2 = '1 1 2 3 4 4 4 5 5'
test_string_3 = '2*1 2 3 3*4 2*5'
test_string_4 = '0 1 2 2 3 3 3 4 4 4 4 5 5 5 5 5 6 6 6 6 6 6 7 7 7 7 7 7 7 8 8 8 8 8 8 8 8 9 9 9 9 9 9 9 9 9'


def test_expand():
    assert test_string_1 == expand(test_string_1)
    assert expand(test_string_3) == '1 1 2 3 4 4 4 5 5'


def test_compress():
    assert test_string_1 == compress(test_string_1)
    assert compress(test_string_2) == '2*1 2 3 3*4 2*5'
    assert compress(test_string_3) == test_string_3
    assert test_string_4 == expand(compress(test_string_4))
