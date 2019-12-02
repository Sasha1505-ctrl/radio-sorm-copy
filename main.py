# -*- coding: utf-8 -*-
from kaitai.parser.tetra import Tetra
from datetime import datetime
from pprint import pprint
import click


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
        buffer = []
        call_reference = None
        for event in blk.events.event:
            if event.body.type == Tetra.Types.toc:
                """ Обработка записи инициализации вызова TOC """
                pprint(event.body.seq_num)
                if call_reference is not None:
                    pprint(f"Last ref is {call_reference}")
                    raise IOError("Не ожиданное вхождение записи TOC")
                if event.body.members == 65535:
                    # Обработка персонального вызова
                    if event.body.call_reference == 0:
                        # Звонок не состоялся
                        call_reference = None
                    else:
                        # Продолжаем разбирать звонок
                        call_reference = event.body.call_reference
                else:
                    # Обработка группового вызова
                    call_reference = None
            if event.body.type == Tetra.Types.tcc:
                """ Обработка запси терминации вызова TCC """
                pprint(event.body.seq_num)
                if call_reference is None:
                    pprint(f"Last ref is {call_reference}")
                    raise IOError("Неккоректная последовательность записей TOC -> TCC")
                call_reference = None
            if event.body.type == Tetra.Types.out_g:
                """ Обработка записи звонка исходящего на фиксированную сеть """
                if call_reference is None:
                    raise IOError("Некорректная последовательность записей TOC -> OUT_G")
                call_reference = None
            if event.body.type == Tetra.Types.in_g:
                """ Обработка записи звонка пришедшего с внешней сети """
                pprint(event.body.seq_num)
                if call_reference is not None:
                    pprint(f"Last ref is {call_reference}")
                    raise IOError("Не ожиданное вхождение записи TOC")
                if event.body.call_reference == 0:
                    # Звонок не состоялся
                    # Скорее всего для ИС Январь необходимо фиксировать несостоявшиеся звонки
                    call_reference = None
                else:
                    # Продолжаем обрабатывать звонок
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
