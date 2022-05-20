from utility import *
from datetime import timedelta

import pytest


def test_dec_to_sec():
    assert timedelta(seconds=1) == to_sec(100)


def test_str_to_sec():
    with pytest.raises(TypeError):
        to_sec("hellp")


def test_bcd_to_str_con():
    src = b"\x10\x20\x25\x00\x00\x75\x78\x00\x46\xff"
    assert bcd_to_str(src) == "102025000075780046ff"
