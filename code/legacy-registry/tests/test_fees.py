from registry.app import calc_fee


def test_single_transcript():
    assert calc_fee("transcript", 1, False) == 5000


def test_two_letters():
    assert calc_fee("letter", 2, False) == 4000
