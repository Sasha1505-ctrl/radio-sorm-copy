from sorm.utility import * 
import pytest

def test_dec_to_sec():
    assert 1 == to_sec(100)

@pytest.mark.xfail(raises=TypeError)
def test_str_to_sec():
    assert 1 == to_sec("hellp")