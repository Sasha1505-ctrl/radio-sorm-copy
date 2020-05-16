import ftplib
import io
import os
import re
from datetime import datetime, timedelta

last_cdr: str = ''

def callback(info):
    ls_out = info.split()
    if re.match(r'CF\d{4}.D00', ls_out[-1]):
        td = datetime.now() - datetime.strptime(" ".join(ls_out[:2]), '%H.%M:%S %d.%m.%Y') 
        if td <= timedelta(minutes=15):
            global last_cdr
            last_cdr = ls_out[-1]
    return None

ftp = ftplib.FTP('172.20.137.66')
ftp.login('FTPPTF', 'PTFFTP')
ftp.cwd('VIDAST')
ls = ftp.retrlines('LIST ' + 'CF*', callback)
print(f'last_cdr is {last_cdr}')
local_cdr = open(last_cdr, 'wb')
ftp.retrbinary('RETR ' + last_cdr, local_cdr.write)
ftp.quit()
