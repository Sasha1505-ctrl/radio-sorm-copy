from sorm.utility import * 
import pytest

def test_dec_to_sec():
    assert 1 == to_sec(100)

@pytest.mark.xfail(raises=TypeError)
def test_str_to_sec():
    assert 1 == to_sec("hellp")

def test_bcd_to_str_con():
    src = b'\x10\x20\x25\x00\x00\x75\x78\x00\x46\xff'
    assert bcd_to_str(src) == '102025000075780046ff'