from datetime import datetime, timedelta
from binascii import b2a_hex
import logging
from configparser import ConfigParser, ExtendedInterpolation
from pathlib import Path


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


def set_variables(ptus):
    BASE_DIR = Path(__file__).resolve().parent.parent
    # Определяем имя файла журнала
    config = ConfigParser(interpolation=ExtendedInterpolation())
    config.read(f'{BASE_DIR}/config.properties')

    log_file = BASE_DIR.joinpath(config.get(ptus, 'log'), 'processing.log')
    log_file.parent.mkdir(parents=True, exist_ok=True)

    data_out = BASE_DIR.joinpath(config.get(ptus, 'result'))
    data_out.mkdir(parents=True, exist_ok=True)
    tetra_version: int = int(config.get(ptus, 'version'))
    provider_id: int = int(config.get(ptus, 'ptus_id'))

    return {
        'log': log_file,
        'data': data_out,
        'dxt_release': tetra_version,
        'provider_id': provider_id
        }


_log_format = f'%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s'


def get_file_handler(filename):
    file_handler = logging.FileHandler(filename)
    file_handler.setLevel(logging.WARNING)
    file_handler.setFormatter(logging.Formatter(_log_format))
    return file_handler


def get_stream_handler():
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(logging.Formatter(_log_format))
    return stream_handler


def get_logger(filename):
    logger = logging.getLogger(__file__)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(get_file_handler(filename))
    logger.addHandler(get_stream_handler())
    return logger
