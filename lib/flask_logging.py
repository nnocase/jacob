# -*- coding:utf-8 -*-
"""
Description: 系统监控报错邮件
Date: 2020-03-12
Author: xgf
"""
import os
import sys
import random
import string
import logging
import logging.handlers
from importlib import reload
from flask import request, current_app

reload(sys) 

def get_ip_address(ifname='eth1'):
    import socket
    import fcntl
    import struct
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915, # SIOCGIFADDR  
            struct.pack('256s', ifname[:15])
        )[20:24])
    except:
        return ''

ip = get_ip_address()


try:
    #server = os.environ["HOSTNAME"]
    import socket
    server = socket.gethostname()
except:
    server = "unkown"


def emit(self, record):
    """
    Overwrite the logging.handlers.SMTPHandler.emit function with SMTP_SSL.
    Emit a record.
    Format the record and send it to the specified addressees.
    """
    try:
        import smtplib
        from email.utils import formatdate
        port = self.mailport
        if not port:
            port = smtplib.SMTP_PORT
        smtp = smtplib.SMTP_SSL(self.mailhost, port, timeout=5)
        real_ip = request.headers.get("X-Real-Ip", "")
        ref = request.headers.get("Referer", "")
        header = "From: %s(%s)\r\n\r\nX-Real-Ip:%s\r\nReferer:%s\r\n" % (server, ip, real_ip, ref)
        msg = self.format(record)
        msg = msg = header + "%s\r\n%s\r\n%s\r\n%s\r\n" % (ip, request.url, request.data, request.values.to_dict()) + self.format(record)
        msg = "From: %s\r\nTo: %s\r\nSubject: %s\r\nDate: %s\r\n\r\n%s" % (self.fromaddr, ", ".join(self.toaddrs), self.getSubject(record), formatdate(), msg)
        if self.username:
            smtp.ehlo()
            smtp.login(self.username, self.password)
        smtp.sendmail(self.fromaddr, self.toaddrs, msg)
        smtp.quit()
    except (KeyboardInterrupt, SystemExit):
        raise
    except:
        self.handleError(record)


def enable_logging(app):
    print(">>>>>>>>>>>>日志系统",)
    logging.handlers.SMTPHandler.emit = emit
    config = app.config['LOGGING']
    config_mail = config.get('SMTP')
    if config_mail: # 如果存在smtp配置
        app.logger.info('Add SMTP Logging Handler')
        mail_handler = logging.handlers.SMTPHandler(
            (config_mail['HOST'],config_mail['PORT']),  # smtp 服务器地址
            config_mail['USER'], # smtp 发件人
            config_mail['TOADDRS'], # smtp 收件人
            config_mail['SUBJECT'], # smtp 主题
            (config_mail['USER'],config_mail['PASSWORD'])) # smtp账号密码
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)
    else:
        app.logger.info('No SMTP Config Found')
    config_file = config.get('FILE')
    if config_file: # 如果存在文件配置
        app.logger.info( 'Add File Logging Handler' )
        file_handler = logging.handlers.RotatingFileHandler(
            config_file['PATH'], # 文件路径
            # 但个文件大小 默认10M 
            maxBytes  = config_file.setdefault('MAX_BYTES',1024 * 1024 * 10), 
            # 文件备份>数量 默认5个
            backupCount = config_file.setdefault('BACKUP_COUNT',5), 
        )
        logging.basicConfig(level=logging.INFO)
        file_handler.setLevel(logging.INFO)
        formatter = logging.Formatter('[%(asctime)s | %(levelname)s | %(funcName)s] %(message)s')
        file_handler.setFormatter(formatter)
        app.logger.addHandler(file_handler)
    else:
        app.logger.info('No FILE Config Found')
