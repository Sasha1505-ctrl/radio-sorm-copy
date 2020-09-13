# -*- coding: utf-8 -*-
from typing import List, Tuple, DefaultDict
from collections import deque, defaultdict
import click
import csv
import logging
from cdr import Gcdr, Subscriber, Dvo, Interfacez, UserType, CallType, Reg
from sqlalchemy import create_engine
from configparser import ConfigParser, ExtendedInterpolation
from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    DateTime,
    MetaData,
    PrimaryKeyConstraint,
)
from pprint import pprint
from pathlib import Path
from enum import Enum

from utility import bcd_to_str, bcd_to_time, to_sec

UNDEFINED_LOCATION: int = 0
LOG = None  # initialized in init_logging
BASE_DIR = Path(__file__).resolve().parent.parent


@click.command()
@click.argument('files', nargs=-1, type=click.Path(exists=True))
@click.option(
    '--ptus', type=click.Choice(['SK', 'SV', 'VV', 'PO', 'PI'], case_sensitive=False)
)
def main(files, ptus):

    config = ConfigParser(interpolation=ExtendedInterpolation())
    config.read(f'{BASE_DIR}/config.properties')

    data_out = BASE_DIR.joinpath(config.get(ptus, 'result'))
    data_out.mkdir(parents=True, exist_ok=True)
    log_file = BASE_DIR.joinpath(config.get(ptus, 'log'))
    log_file.parent.mkdir(parents=True, exist_ok=True)
    tetra_version: Integer = int(config.get(ptus, 'version'))
    provider_id = int(config.get(ptus, 'ptus_id'))

    # append log files if DEBUG is set (from top of file)
    init_logging(log_file, True)

    global LOG
    LOG = logging.getLogger(__name__)

    for path in Path.cwd().glob(files):
        out_buffers: Tuple[List[Gcdr], DefaultDict[str, List[Reg]]] = cdr_parser(path, tetra_version, provider_id)
        write_to_csv(out_buffers, f"{data_out}/{Path(path).name}")


def init_logging(log_file=None, append=False, console_loglevel=logging.INFO):
    """Set up logging to file and console."""
    if log_file is not None:
        if append:
            filemode_val = "a"
        else:
            filemode_val = "w"
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s %(levelname)s %(threadName)s %(name)s %(message)s",
            # datefmt='%m-%d %H:%M',
            filename=log_file,
            filemode=filemode_val,
        )
    # define a Handler which writes INFO messages or higher to the sys.stderr
    console = logging.StreamHandler()
    console.setLevel(console_loglevel)
    # set a format which is simpler for console use
    formatter = logging.Formatter("%(message)s")
    console.setFormatter(formatter)
    # add the handler to the root logger
    logging.getLogger("").addHandler(console)
    global LOG
    LOG = logging.getLogger(__name__)


def cdr_parser(
    filename, version: Integer, provider_id: Integer
) -> Tuple[List[Gcdr], DefaultDict[str, List[Reg]]]:

    LOG.info(f"Пытаюсь разобрать {filename} при помощи {version} версии парсера")

    if version == 5:
        from kaitai.parser.tetra_v5 import Tetra
    elif version == 7:
        from kaitai.parser.tetra_v7 import Tetra
    else:
        raise Exception("Не удалось загрузить модуль парсера")

    target = Tetra.from_file(filename)

    call_stack = deque()
    reg_buffer: DefaultDict[str, List[Reg]] = defaultdict(list)
    cdr_buffer: List[Gcdr] = []

    class MockUi(Enum):
        Inner = 1

    class MockInt:
        def __init__(self):
            self.ui = MockUi.Inner
            self.pui_type = 0
            self.pui_index = 0

    void_int = Interfacez(MockInt())

    for blk in target.block:
        LOG.info("Starting new block in CDR file")
        for event in blk.events.event:
            pprint(event)
            if event.body.type == Tetra.Types.toc:
                """ Обработка записи инициализации вызова TOC """
                if len(call_stack) != 0:
                    raise ValueError(
                        f"Неожиданное вхождение записи TOC."
                        f"Обработка звонка {event.body.call_reference}"
                        f"завершена не корректно."
                    )
                LOG.debug(f"TOC: {event.body.seq_num} cr: {event.body.call_reference}")
                if event.body.members == 65535:
                    # Обработка персонального вызова
                    if event.body.call_reference == 0:
                        # Звонок не состоялся. Строим GCDR и сохраняем в CSV
                        toc: Tetra.Toc = event.body
                        userA = Subscriber(
                            UserType.inner,
                            bcd_to_str(toc.served_number),
                            toc.location,
                            toc.location,
                        )
                        userB = Subscriber(
                            UserType.inner,
                            bcd_to_str(toc.called_number),
                            UNDEFINED_LOCATION,
                            UNDEFINED_LOCATION,
                        )
                        dvo = Dvo(False)
                        gdp = Gcdr(
                            toc.dxt_id.as_int,
                            provider_id,
                            bcd_to_time(toc.setup_time),
                            to_sec(toc.duration),
                            userA,
                            userB,
                            void_int,
                            void_int,
                            toc.termination,
                            dvo,
                            CallType.toc,
                        )
                        cdr_buffer.append(gdp)
                    else:
                        # Звонок состоялся. Инициализируем GCDR и ждем TCC или OutG
                        call_stack.append(event.body)
                else:
                    # Обработка группового вызова. Строим GCDR и сохраняем его в CSV
                    toc = event.body
                    userA = Subscriber(
                        UserType.inner,
                        bcd_to_str(toc.served_number),
                        toc.location,
                        toc.location,
                    )
                    userB = Subscriber(
                        UserType.inner,
                        bcd_to_str(toc.called_number),
                        UNDEFINED_LOCATION,
                        UNDEFINED_LOCATION,
                    )
                    dvo = Dvo(False)
                    gdp = Gcdr(
                        toc.dxt_id.as_int,
                        provider_id,
                        bcd_to_time(toc.setup_time),
                        to_sec(toc.duration),
                        userA,
                        userB,
                        void_int,
                        void_int,
                        toc.termination,
                        dvo,
                        CallType.toc,
                    )
                    cdr_buffer.append(gdp)
            if event.body.type == Tetra.Types.tcc:
                """ Обработка запси терминации вызова TCC """
                if len(call_stack) == 0:
                    raise ValueError(
                        f"Не обработана запись "
                        f"TOC или InG для звонка {event.body.call_reference}"
                    )
                LOG.debug(f"TCC: {event.body.seq_num} cr: {event.body.call_reference}")
                partial_cdr = call_stack.pop()
                if partial_cdr.call_reference == event.body.call_reference:
                    """Все совпало. Будем собирать Gcdr"""
                    tcc = event.body
                    dvo = Dvo(False)
                    if type(partial_cdr) is Tetra.Toc:
                        userA = Subscriber(
                            UserType.inner,
                            bcd_to_str(partial_cdr.served_number),
                            partial_cdr.location,
                            UNDEFINED_LOCATION,
                        )
                        userB = Subscriber(
                            UserType.inner,
                            bcd_to_str(tcc.served_number),
                            tcc.location,
                            UNDEFINED_LOCATION,
                        )
                        gdp = Gcdr(
                            partial_cdr.dxt_id.as_int,
                            provider_id,
                            bcd_to_time(partial_cdr.setup_time),
                            to_sec(partial_cdr.duration),
                            userA,
                            userB,
                            void_int,
                            void_int,
                            partial_cdr.termination,
                            dvo,
                            CallType.toctcc,
                        )
                        cdr_buffer.append(gdp)
                    elif type(partial_cdr) is Tetra.InG:
                        userA = Subscriber(
                            UserType.outer,
                            bcd_to_str(partial_cdr.calling_number),
                            UNDEFINED_LOCATION,
                            UNDEFINED_LOCATION,
                        )
                        userB = Subscriber(
                            UserType.inner,
                            bcd_to_str(tcc.served_nitsi),
                            tcc.location,
                            UNDEFINED_LOCATION,
                        )
                        gdp = Gcdr(
                            tcc.dxt_id.as_int,
                            provider_id,
                            bcd_to_time(tcc.setup_time),
                            to_sec(tcc.duration),
                            userA,
                            userB,
                            Interfacez(partial_cdr.in_int),
                            void_int,
                            tcc.termination,
                            dvo,
                            CallType.ingtcc,
                        )
                        cdr_buffer.append(gdp)
                    else:
                        raise ValueError(f"Неожиданный тип объекта {type(partial_cdr)}")
                else:
                    raise ValueError(
                        f"Не соответствие call_reference обрабатываемых записей"
                        f"{partial_cdr.call_reference} != {event.body.call_reference}"
                    )
            if event.body.type == Tetra.Types.out_g:
                """Обработка записи звонка исходящего на фиксированную сеть TOC -> OutG"""
                if len(call_stack) == 0:
                    raise ValueError(
                        f"Не обработана запись TOC для звонка {event.body.call_reference}"
                    )
                LOG.debug(f"OutG: {event.body.seq_num} cr: {event.body.call_reference}")
                toc: Tetra.Toc = call_stack.pop()
                out_g: Tetra.OutG = event.body
                userA = Subscriber(
                    UserType.inner,
                    bcd_to_str(toc.served_number),
                    toc.location,
                    UNDEFINED_LOCATION,
                )
                userB = Subscriber(
                    UserType.outer,
                    bcd_to_str(out_g.transmitted_number),
                    UNDEFINED_LOCATION,
                    UNDEFINED_LOCATION,
                )
                dvo = Dvo(False)
                gdp = Gcdr(
                    toc.dxt_id.as_int,
                    provider_id,
                    bcd_to_time(toc.setup_time),
                    to_sec(toc.duration),
                    userA,
                    userB,
                    void_int,
                    Interfacez(out_g.out_int),
                    toc.termination,
                    dvo,
                    CallType.tocoutg,
                )
                cdr_buffer.append(gdp)
            if event.body.type == Tetra.Types.in_g:
                """ Обработка записи звонка пришедшего из внешней сети """
                if len(call_stack) != 0:
                    raise ValueError(
                        f"Неожиданное вхождение записи IN_G."
                        f"Обработка звонка {event.body.call_reference}"
                        f"завершена не корректно."
                    )
                LOG.debug(f"InG: {event.body.seq_num} cr: {event.body.call_reference}")
                if event.body.call_reference == 0:
                    # Звонок не состоялся. Строим GCDR и сохраняем его в CSV
                    in_g: Tetra.InG = event.body
                    userA = Subscriber(
                        UserType.outer,
                        bcd_to_str(in_g.calling_number),
                        UNDEFINED_LOCATION,
                        UNDEFINED_LOCATION,
                    )
                    userB = Subscriber(
                        UserType.inner,
                        bcd_to_str(in_g.called_number),
                        UNDEFINED_LOCATION,
                        UNDEFINED_LOCATION,
                    )
                    dvo = Dvo(False)
                    gdp = Gcdr(
                        in_g.dxt_id.as_int,
                        provider_id,
                        bcd_to_time(in_g.setup_time),
                        to_sec(in_g.duration),
                        userA,
                        userB,
                        Interfacez(in_g.in_int),
                        void_int,
                        in_g.termination,
                        dvo,
                        CallType.ing,
                    )
                    cdr_buffer.append(gdp)
                else:
                    # Продолжаем обрабатывать звонок
                    call_stack.append(event.body)

            if event.body.type == Tetra.Types.reg:
                """ Обработка записи о регистрации абонента """
                LOG.debug(
                    f"REG: {event.body.seq_num}"
                    f"SERVED_NITSI: {bcd_to_str(event.body.served_nitsi)}"
                    f"LOCATION: {event.body.location}:{event.body.prev_location}"
                )
                reg = Reg(event.body)
                reg_buffer[reg.get_number()].append(reg)
        LOG.info(
            f"End reading block. Calls quantity: {len(cdr_buffer)}."
            f"Regs quantity: {len(reg_buffer)}"
        )
        # Write REG records to BD

        # if len(reg_buffer) > 0:
        #   conn.execute(REGS_TABLE.insert(), reg_buffer)
        #   reg_buffer.clear()
    return cdr_buffer, reg_buffer


def init_db(path):
    engine = create_engine(f"sqlite:///{path}", echo=True)
    metadata = MetaData()

    regs_table = Table(
        "regs",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("served_nitsi", String(12)),
        Column("location", Integer),
        Column("prev_location", Integer),
        Column("reg_at", DateTime),
        PrimaryKeyConstraint("id", "served_nitsi", name="reg_pk"),
    )

    metadata.create_all(engine)
    conn = engine.connect()
    return conn, regs_table


def write_to_csv(
    out_buffers: Tuple[List[Gcdr], DefaultDict[str, List[Reg]]], file: str
):
    cdr_buff, reg_buff = out_buffers
    # Write gcdrs to file
    with open(file, "w+", newline="") as csv_file:
        wr = csv.writer(csv_file, delimiter=";")
        for cdr in cdr_buff:
            cdr.abon_a.get_last_location(reg_buff, cdr.date, cdr.call_duration)
            cdr.abon_b.get_last_location(reg_buff, cdr.date, cdr.call_duration)
            wr.writerow(list(cdr))


if __name__ == "__main__":
    main()
