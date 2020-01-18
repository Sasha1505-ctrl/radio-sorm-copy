# -*- coding: utf-8 -*-
from kaitai.parser.tetra import Tetra
from datetime import datetime
from pprint import pprint
from typing import Optional
from collections import deque
import click
from cdr import Gcdr, Subscriber, Dvo

def bcdDigits(chars):
    for char in chars:
        char = ord(char)
        for val in (char >> 4, char & 0xF):
            if val == 0xF:
                return
            yield val


@click.command()
@click.argument('filename', type=click.Path(exists=True))
def parseCDR(filename):

    from sqlalchemy import create_engine
    engine = create_engine('sqlite:///test.db', echo=True)

    from sqlalchemy import Table, Column, Integer, String, DateTime, MetaData,    PrimaryKeyConstraint
    metadata = MetaData()
    regs = Table(
            'regs', metadata,
            Column('id', Integer, primary_key=True),
            Column('served_nitsi', String(12)),
            Column('location', Integer),
            Column('prev_location', Integer),
            Column('reg_at', DateTime),
            PrimaryKeyConstraint('id', 'served_nitsi', name='reg_pk')
            )
    metadata.create_all(engine)

    target = Tetra.from_file(filename)

    conn = engine.connect()
    for blk in target.block:
        # conn.execute(
        #     regs.insert(),
        #     [
        #         dict(
        #             id=event.body.seq_num,
        #             served_nitsi="".join([hex(i)[2:] for i in event.body.served_nitsi]),
        #             location=event.body.location,
        #             prev_location=event.body.prev_location,
        #             reg_at=datetime(
        #                 event.body.timestamp.full_year,
        #                 event.body.timestamp.month.as_int,
        #                 event.body.timestamp.day.as_int,
        #                 event.body.timestamp.hour.as_int,
        #                 event.body.timestamp.min.as_int,
        #                 event.body.timestamp.sec.as_int,
        #                 event.body.timestamp.msec.as_int),
        #             )
        #         for event in blk.events.event if event.body.type == Tetra.Types.reg
        #     ]
        # )
        callStack = deque()
        buffer = []
        call_reference: Optional[int] = None
        for event in blk.events.event:
            if event.body.type == Tetra.Types.toc:
                """ Обработка записи инициализации вызова TOC """
                if call_reference is not None:
                   raise ValueError(f'Неожиданное вхождение записи TCC. Обработка звонка {call_reference} завершена не корректно.')
                
                if event.body.members == 65535:
                    # Обработка персонального вызова
                    if event.body.call_reference == 0:
                        # Звонок не состоялся. Строим GCDR и сохраняем в CSV
                        toc = event.body
                        userA = Subscriber(0, toc.served_number, toc.location, toc.location)
                        userB = Subscriber(0, toc.called_number, '255', '255')
                        dvo = Dvo(False)
                        gcdr = Gcdr(toc.dxt_id, '23', toc.setup_time, toc.duration, userA, userB, 0, 0, toc.termination, dvo)
                        pprint(gcdr)
                        call_reference = None
                    else:
                        # Звонок состоялся. Инициализируем GCDR и ждем TCC
                        callStack.append(event.body)
                        call_reference = event.body.call_reference
                else:
                    # Обработка группового вызова. Строим GCDR и сохраняем его в CSV
                    call_reference = None
            if event.body.type == Tetra.Types.tcc:
                """ Обработка запси терминации вызова TCC """
                if call_reference is None:
                    raise ValueError(f'Не обработана запис TOC или InG для звонка {call_reference}')
                if call_reference == event.body.call_reference:
                    """Все совпало. Будем собирать Gcdr"""
                    pprint(event.body.seq_num)
                    partial_cdr = callStack.pop()
                    tcc = event.body
                    dvo = Dvo(False)
                    if type(partial_cdr) is Tetra.Toc:
                        userA = Subscriber(0, partial_cdr.served_number, partial_cdr.location, partial_cdr.location)
                        userB = Subscriber(0, tcc.served_number, tcc.location, tcc.location)
                        gcdr = Gcdr(partial_cdr.dxt_id, '23', partial_cdr.setup_time, partial_cdr.duration, userA, userB, 0, 0, partial_cdr.termination, dvo)
                        pprint(gcdr)
                    elif type(partial_cdr) is Tetra.InG:
                        userA = Subscriber(1, partial_cdr.calling_number, '255', '255')
                        userB = Subscriber(0, tcc.served_nitsi, tcc.location, tcc.location)
                        gcdr = Gcdr(tcc.dxt_id, '23', tcc.setup_time, tcc.duration, userA, userB, 0, 0, tcc.termination, dvo)
                        pprint(gcdr)
                    else:
                        raise ValueError(f'Вхождение объекта неожиданного типа')
                call_reference = None
            if event.body.type == Tetra.Types.out_g:
                """ Обработка записи звонка исходящего на фиксированную сеть """
                if call_reference is None:
                    raise ValueError(f'Не обработана запись TOC для звонка {call_reference}')
                call_reference = None
            if event.body.type == Tetra.Types.in_g:
                """ Обработка записи звонка пришедшего из внешней сети """
                pprint(event.body.seq_num)
                if call_reference is not None:
                    raise ValueError(f'Неожиданное вхождение записи IN_G. Обработка звонка {call_reference} завершена не корректно.')
                if event.body.call_reference == 0:
                    # Звонок не состоялся. Строим GCDR и сохраняем его в CSV
                    call_reference = None
                else:
                    # Продолжаем обрабатывать звонок
                    callStack.append(event.body)
                    call_reference = event.body.call_reference

            if event.body.type == Tetra.Types.reg:
                """ Обработка записи о регистрации абонента """
                served_nitsi = "".join([hex(i)[2:] for i in event.body.served_nitsi])
                vdate_obj = event.body.timestamp

                buffer.append(
                    dict(
                        id = event.body.seq_num,
                        served_nitsi = served_nitsi,
                        location = event.body.location,
                        prev_location = event.body.prev_location,
                        reg_at = datetime(
                            event.body.timestamp.full_year,
                            event.body.timestamp.month.as_int,
                            event.body.timestamp.day.as_int,
                            event.body.timestamp.hour.as_int,
                            event.body.timestamp.min.as_int,
                            event.body.timestamp.sec.as_int,
                            event.body.timestamp.msec.as_int
                        ),
                    )
                )
        conn.execute(regs.insert(), buffer)
        buffer = []


if __name__ == '__main__':
    parseCDR()
