# -*- coding: utf-8 -*-
from ftplib import FTP
from config import host, port, login, password

out = 'Game_log_file.log'
out2 = 'old_Game_log_file.log'


def download_log(a: bool, b: bool) -> str:
    if a is False and b is False:
        return 'Поставьте галочку'
    with FTP() as ftp:
        ftp.connect(host, port)
        ftp.login(login, password)
        ftp.cwd('185.66.84.228_27015-Saved/Logs')
        dir = ftp.nlst()
        if a is True:
            with open(out, 'wb') as f:
                ftp.retrbinary('RETR ' + dir[-1], f.write)
            return 'Game_log_file.log'
        if b is True:
            with open(out2, 'wb') as f:
                ftp.retrbinary('RETR ' + dir[-2], f.write)
            return 'old_Game_log_file.log'