# -*- coding: utf-8 -*-
import traceback
from typing import List, Tuple, DefaultDict
from collections import deque, defaultdict
import click, csv, sys
from cdr import Gcdr, Subscriber, Dvo, Interfacez, UserType, CallType, Reg
from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    DateTime,
    MetaData,
    PrimaryKeyConstraint,
    create_engine,
)
from pathlib import Path
from enum import Enum

from utility import get_logger, set_variables, bcd_to_str, bcd_to_time, to_sec

from pprint import pprint
UNDEFINED_LOCATION: int = 0

import mysql.connector
from mysql.connector import Error


@click.command()
@click.argument('files', nargs=-1, type=click.Path(exists=True))
@click.option(
    '--ptus', type=click.Choice(['SK', 'SV', 'VV', 'PO', 'PI'], case_sensitive=False)
)
def main(files, ptus):
    var_dict = set_variables(ptus)
    logger = get_logger(var_dict.get('log'))

    for cdr_file in files:
        logger.info(f'Processing {cdr_file}')
        path = Path(cdr_file)
        try:
            out_buffers: Tuple[List[Gcdr], DefaultDict[str, List[Reg]]] = cdr_parser(
                path,
                var_dict.get('dxt_release'),
                var_dict.get('provider_id'),
                logger
                )
            write_to_csv(out_buffers, f'{var_dict.get("data")}/{Path(path).name}')
        except ValueError as err:
            logger.error(err)
        except AttributeError as err:
            logger.error(f'Check Tetra software release. {err}')
            track = traceback.format_exc()
            print(track)
        except Exception as exp:
            logger.error(f'No Tetra format or file corrupted {exp}')

def cdr_parser(
    filename, version: int, provider_id: int, logger
) -> Tuple[List[Gcdr], DefaultDict[str, List[Reg]]]:

    logger.debug(f"Пытаюсь разобрать {filename} при помощи {version} версии парсера")
    if version == 5:
        from kaitai.parser.tetra_v5 import Tetra
    elif version == 7:
        from kaitai.parser.tetra_v7 import Tetra
    else:
        logger.error(f'Не удалось загрузить модуль парсера')
        raise Exception("Не удалось загрузить модуль парсера")

    target = Tetra.from_file(filename)

    call_stack = deque()
    reg_buffer: DefaultDict[str, List[Reg]] = defaultdict(list)
    cdr_buffer: List[Gcdr] = []

    class MockUi(Enum):
        Inner = 0

    class MockInt:
        def __init__(self):
            self.ui = MockUi.Inner
            self.pui_type = 0
            self.pui_index = 0

    void_int = Interfacez(MockInt())

    conn = connect_to_db()

    for blk in target.block:
        logger.debug(f'Starting new block {blk.header.block_num} in CDR file')
        for event in blk.events.event:
            if event.body.type == Tetra.Types.toc:
                """ Обработка записи инициализации вызова TOC """
                if call_stack:
                    rec = call_stack.pop()
                    logger.error(f'Неожиданное вхождение TOC записи в {filename}.'
                                 f'Call stack member is {rec.type} -> '
                                 f'cr: {rec.call_reference}')
                logger.debug(f'TOC: {event.body.seq_num} cr: {event.body.call_reference}')
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
                            logger,
                        )
                        userB = Subscriber(
                            UserType.inner,
                            bcd_to_str(toc.called_number),
                            UNDEFINED_LOCATION,
                            UNDEFINED_LOCATION,
                            logger,
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
                        logger,
                    )
                    userB = Subscriber(
                        UserType.inner,
                        bcd_to_str(toc.called_number),
                        UNDEFINED_LOCATION,
                        UNDEFINED_LOCATION,
                        logger,
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
                if not call_stack:
                    logger.error(f'Не обработаны записи TOC или InG для звонка'
                                 f'{event.body.type} -> cr: {event.body.call_reference}')
                    continue

                logger.debug(f"TCC: {event.body.seq_num} cr: {event.body.call_reference}")
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
                            logger,
                        )
                        userB = Subscriber(
                            UserType.inner,
                            bcd_to_str(tcc.served_number),
                            tcc.location,
                            UNDEFINED_LOCATION,
                            logger,
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
                            logger,
                        )
                        userB = Subscriber(
                            UserType.inner,
                            bcd_to_str(tcc.served_nitsi),
                            tcc.location,
                            UNDEFINED_LOCATION,
                            logger,
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
                logger.debug(f"OutG: {event.body.seq_num} cr: {event.body.call_reference}")
                toc: Tetra.Toc = call_stack.pop()
                out_g: Tetra.OutG = event.body
                userA = Subscriber(
                    UserType.inner,
                    bcd_to_str(toc.served_number),
                    toc.location,
                    UNDEFINED_LOCATION,
                    logger,
                )
                userB = Subscriber(
                    UserType.outer,
                    bcd_to_str(out_g.transmitted_number),
                    UNDEFINED_LOCATION,
                    UNDEFINED_LOCATION,
                    logger,
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
                logger.debug(f"InG: {event.body.seq_num} cr: {event.body.call_reference}")
                if event.body.call_reference == 0:
                    # Звонок не состоялся. Строим GCDR и сохраняем его в CSV
                    in_g: Tetra.InG = event.body
                    userA = Subscriber(
                        UserType.outer,
                        bcd_to_str(in_g.calling_number),
                        UNDEFINED_LOCATION,
                        UNDEFINED_LOCATION,
                        logger,
                    )
                    userB = Subscriber(
                        UserType.inner,
                        bcd_to_str(in_g.called_number),
                        UNDEFINED_LOCATION,
                        UNDEFINED_LOCATION,
                        logger,
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
                logger.debug(
                    f"REG: {event.body.seq_num} "
                    f"SERVED_NITSI: {bcd_to_str(event.body.served_nitsi)} "
                    f"LOCATION: {event.body.location}:{event.body.prev_location}"
                )
                reg = Reg(event.body)
                reg_buffer[reg.get_number()].append(reg)

                write_data (reg.get_number(), bcd_to_time(event.body.timestamp), conn)


            if event.body.type == Tetra.Types.sms:
                """ Обработка записи о текстовом сообщении """
                logger.debug("I'am find SMS")
                sds: Tetra.Sds = event.body
                userA = Subscriber(
                     UserType.inner,
                     bcd_to_str(sds.served_number),
                     sds.location,
                     sds.location,
                     logger,
                )
                userB = Subscriber(
                   UserType.inner,
                   bcd_to_str(sds.connected_number),
                   UNDEFINED_LOCATION,
                   UNDEFINED_LOCATION,
                   logger,
                )
                dvo = Dvo(False)
                gdp = Gcdr(
                    sds.dxt_id.as_int,
                    provider_id,
                    bcd_to_time(sds.time_stamp),
                    to_sec(0),
                    userA,
                    userB,
                    void_int,
                    void_int,
                    sds.sds_type,
                    dvo,
                    CallType.sms,
                )
                cdr_buffer.append(gdp)

        logger.info(
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

def connect_to_db():
    """ connect_to_db to MySQL database """
    conn = None
    try:
        conn = mysql.connector.connect(host='172.20.132.239:3306',
                                       database='last_reg_db',
                                       user='root',
                                       password='root')
        if conn.is_connected():
            #print('connect_to_db to MySQL database')
            return conn


    except Error as e:
        print(e)


def write_data (issi, data, conn):

    try:
        cursor = conn.cursor()
        query = ""

        query = ("INSERT INTO registration"
            "(ISSI, DATE_TIME, METRIC) "
            "VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE DATE_TIME=%s, METRIC=%s")
        data_query= (issi, data, issi, data, issi)
        print (data_query)
        cursor.execute(query, data_query)
        conn.commit()

        query = ("INSERT INTO all_registration"
            "(ISSI, DATE_TIME, METRIC) "
            "VALUES (%s, %s, %s)")
        #print(query)
        data_query= (1, data, issi)
        #print (data_query)

        cursor.execute(query, data_query)
        conn.commit()

    except Error as e:
        print(e)



if __name__ == "__main__":
    main()
