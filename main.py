from tetra import *
from datetime import datetime, date, time
from pprint import pprint

def bcdDigits(chars):
    for char in chars:
        char = ord(char)
        for val in (char >> 4, char & 0xF):
            if val == 0xF:
                return
            yield val

target = Tetra.from_file("CF0795.D00")
from sqlalchemy import create_engine
engine = create_engine('sqlite:///test.db',echo=True)

from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
metadata = MetaData()
regs = Table('regs', metadata,
        Column('id', Integer, primary_key=True),
        Column('served_nitsi', String(12)),
        Column('location', Integer),
        Column('prev_location', Integer),
        )
metadata.create_all(engine)
conn = engine.connect()

for blk in target.block:
    for event in blk.events.event:
        if event.body.type == Tetra.Types.reg:
            served_nitsi = "".join([hex(i)[2:] for i in event.body.served_nitsi])
            ins = regs.insert().values(served_nitsi=served_nitsi,
                    location=event.body.location,
                    prev_location=event.body.prev_location)
            result = conn.execute(ins)

            date_obj = event.body.timestamp
            print(datetime(date_obj.full_year, date_obj.month.as_int,
                           date_obj.day.as_int, date_obj.hour.as_int,
                           date_obj.min.as_int, date_obj.sec.as_int,
                           date_obj.msec.as_int))
            print(event.body.location, event.body.prev_location)
            #print("".join([f"{(ord(x)>>4)*10+(ord(x)&0x0F):02}" for x in event.body.served_nitsi]))

