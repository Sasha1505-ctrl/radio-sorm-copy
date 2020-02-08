from datetime import datetime


def bcd_to_str(arr: bytearray) -> str:
    return "".join([hex(i)[2:] for i in arr])


def bcd_to_time(tetra_time) -> datetime:
        return datetime(
            tetra_time.full_year,
            tetra_time.month.as_int,
            tetra_time.day.as_int,
            tetra_time.hour.as_int,
            tetra_time.min.as_int,
            tetra_time.sec.as_int,
            tetra_time.msec.as_int
        )


def to_sec(dec_msec: int) -> int:
    """
    Convert 10 msec unit from Tetra CDR to sec
    dec_msec: unit is 10 milliseconds
    """
    return round(dec_msec/100)