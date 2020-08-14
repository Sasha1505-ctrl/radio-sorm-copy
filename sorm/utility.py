from datetime import datetime, timedelta
from binascii import b2a_hex


def bcd_to_str(arr: bytearray) -> str:
    return str(b2a_hex(arr), "utf-8")


def bcd_to_time(tetra_time) -> datetime:
    """
    Convert tetra calendar_time_t to Python datetime

    :param tetra_time - tetra calendar_time_t BCD representation
    Msec is bullshit! From kudo this field is hundredths of second
    :return: Python datetime object
    """
    ksec_mult = 10000
    return datetime(
        tetra_time.full_year,
        tetra_time.month.as_int,
        tetra_time.day.as_int,
        tetra_time.hour.as_int,
        tetra_time.min.as_int,
        tetra_time.sec.as_int,
        tetra_time.msec.as_int * ksec_mult,
    )


def to_sec(dec_msec: int) -> timedelta:
    """
    Convert 10 msec unit from Tetra CDR to sec
    dec_msec: unit is 10 milliseconds
    """
    return timedelta(seconds=round(dec_msec/100))