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
for blk in target.block:
    for event in blk.events.event:
        if event.body.type == Tetra.Types.reg:
            print("".join([hex(i)[2:] for i in event.body.served_nitsi]))
            date_obj = event.body.timestamp
            print(datetime(date_obj.full_year, date_obj.month.as_int, date_obj.day.as_int, date_obj.hour.as_int, date_obj.min.as_int,
            date_obj.sec.as_int, date_obj.msec.as_int))
            print(event.body.location, event.body.prev_location)
            #print("".join([f"{(ord(x)>>4)*10+(ord(x)&0x0F):02}" for x in event.body.served_nitsi]))