# -*- coding: utf-8 -*-
# @Time    : 2024/02/27 15:10
# @Author  : Anubis

import os
import email
import imaplib
import quopri
import re
import time

import pandas as pd

IMAP_SERVER = 'imap.163.com'
ACCOUNT = 'anubiscl@163.com'
PASSWORD = 'XXX'
FILE_SAVE_PATH = r''


def save_file(file_name, data, save_path=''):
    file_path = os.path.join(save_path, file_name)
    with open(file_path, 'wb') as fp:
        fp.write(data)
    return file_path


class Message(dict):
    """邮件内容存储格式"""


class Email(object):
    # 邮件类型
    All, Unseen, Seen, Recent, Answered, Flagged = "All,Unseen,Seen,Recent,Answered,Flagged".split(',')

    def __init__(self, imap, account, password, file_save_path=''):
        if imap and account and password:
            self.host = imap
            self.account = account
            self.password = password
            self.save_path = file_save_path
            self.imap_server = self.login()

    def login(self):
        imap_server = imaplib.IMAP4_SSL(self.host)
        imap_server.login(self.account, self.password)
        # 解决网易邮箱报错：Unsafe Login. Please contact kefu@188.com for help
        imaplib.Commands["ID"] = ('AUTH',)
        args = ("name", self.account, "contact", self.account, "version", "1.0.0", "vendor", "myclient")
        imap_server._simple_command("ID", str(args).replace(",", "").replace("\'", "\""))
        return imap_server

    def get_email_by_subject(self, email_type, send_date):
        """获取指定的未读邮件,自动下载附件"""
        result_email = {}
        email_list = self.check_email(last_message=False, message_type=self.Unseen, count=10)
        for msg_data in email_list:
            print(u"邮件主题：{subject}\n邮件日期：{date}\n附件列表：{files}\n邮件正文：{content}".format(
                subject=msg_data.get('subject'),
                date=msg_data.get('date'),
                files=msg_data.get('files'),
                content=msg_data.get('content')
            ))
            if email_type == msg_data.get('subject') and send_date < msg_data.get('date'):
                result_email = msg_data
                break
        return result_email

    def get_newest(self):
        """获取最新的未读邮件,自动下载附件"""
        for msg_data in self.check_email(message_type=self.Unseen):
            print(u"邮件主题：{subject}\n邮件日期：{date}\n附件列表：{files}\n邮件正文：{content}".format(
                subject=msg_data.get('subject'),
                date=msg_data.get('date'),
                files=msg_data.get('files'),
                content=msg_data.get('content')
            ))
            print()
            return msg_data

    def check_email(self, last_message=True, message_type="Unseen", count=1):
        """Message status in "All,Unseen,Seen,Recent,Answered,Flagged"
        :param last_message: 返回邮箱最新(最后一封)邮件,默认为True,
        :param message_type: 检索邮件类型,默认为Unseen(未读)邮件,
        :param count: 检出的邮件消息数目 默认为 1
        :return:
        """
        # 选中收件箱
        select_status, info = self.imap_server.select(mailbox='INBOX')
        if select_status != 'OK':
            print(info)
            raise StopIteration
        # 选择邮件类型
        search_status, items = self.imap_server.search(None, message_type)
        if select_status != 'OK':
            print(items)
            raise StopIteration
        message_list = items[0].split()[-1:] if last_message else items[0].split()[:count]
        print("Read messages within the last 30 days,total {0} {1}type message, read {2}".format(len(items[0].split()),
                                                                                                 message_type,
                                                                                                 len(message_list)))
        for message_index in message_list:
            msg_data = Message()
            fetch_status, message = self.imap_server.fetch(message_index, "(RFC822)")
            msg = email.message_from_bytes(message[0][1])

            # 消息日期 格式化
            msg_data['date'] = format_Date(msg['Date'])
            # 消息主题
            message_subject = email.header.decode_header(msg["Subject"])
            msg_data['subject'] = self.str_to_unicode(message_subject[0][0], message_subject[0][1])
            # 消息正文,消息类型,消息附件
            msg_data.update(self.parse_message(msg, save_path=self.save_path))
            yield msg_data

    @staticmethod
    def str_to_unicode(s, encoding=None):
        return str(s, encoding) if encoding else str(s)

    @staticmethod
    def parse_message(msg, save_path=''):
        """解析message并下载附件，返回字典类型"""
        message_content, content_type, suffix = None, None, None
        files = []
        for part in msg.walk():
            if not part.is_multipart():
                content_type = part.get_content_type()
                filename = part.get_filename()
                # 是否有附件
                if filename:
                    file_header = email.header.Header(filename)
                    decode_header = email.header.decode_header(file_header)
                    file_name = decode_header[0][0]
                    data = part.get_payload(decode=True)
                    print('Attachment : ' + file_name)
                    # 保存附件
                    if file_name:
                        save_file(file_name, data, save_path)
                        files.append(file_name)
                else:
                    if content_type in ['text/plain']:
                        suffix = '.txt'
                    if content_type in ['text/html']:
                        suffix = '.htm'
                    if part.get_charsets() is None:
                        message_content = part.get_payload(decode=True)
                    else:
                        message_content = part.get_payload(decode=True).decode(part.get_charsets()[0])
        msg_data = {
            'content': message_content,
            'type': suffix,
            'files': files
        }
        return msg_data


def decode_MIME():
    """MIME字符进行解码"""
    text = """=E5=9B=A0=E4=B8=BA=E4=B8=81=E4=BF=8A=E6=99=96=E5=8F=AA=E8=B7=9F=E7=9D=80= =E9=BA=A6=E8=BF=AA=E5=B0=B1=E4=B8=8D=E5=8F=AF=E8=83=BD=E9=82=A3=E5=88=B0= =E6=80=BB=E5=86=A0=E5=86=9B=E6=88=92=E6=8C=87=EF=BC=8C=E8=80=83=E8=99=91= =E5=88=B0=E6=8A=A4=E7=90=83=E9=97=AE=E9=A2=98=EF=BC=8C=E5=A6=82=E6=9E=9C= =E7=94=A8=E9=BA=A6=E8=BF=AA=E6=8D=A2=E4=BA=A8=E5=88=A9=E7=9A=84=E8=AF=9D= =E8=AF=B4=E4=B8=8D=E5=AE=9A=E5=B0=B1=E8=A1=8C=EF=BC=8C=E5=BD=93=E7=84=B6= =E8=AF=B8=E8=91=9B=E5=AD=94=E6=98=8E=E8=BF=99=E4=B8=AA=E8=80=81=E7=8B=90= =E7=8B=B8=E8=82=AF=E5=AE=9A=E6=98=AF=E7=95=A5=E6=87=82=E8=BF=99=E4=BB=B6= =E4=BA=8B=E7=9A=84=EF=BC=8C=E4=BB=96=E7=AC=AC=E4=B8=80=E4=B8=AA=E4=B8=8D= =E7=AD=94=E5=BA=94=EF=BC=8C=E5=B0=B1=E7=AE=97=E4=BB=96=E7=AD=94=E5=BA=94= =E4=BA=86=EF=BC=8C=E7=BC=9D=E5=B0=8F=E8=82=9B=E8=83=BD=E7=AD=94=E5=BA=94= =E5=90=97=EF=BC=9F=E6=89=80=E4=BB=A5=E8=BF=99=E6=95=B4=E4=BB=B6=E4=BA=8B= =E6=83=85=E7=9A=84=E4=BA=AE=E7=82=B9=E5=B0=B1=E5=9C=A8=E4=BA=8E=E7=A7=A6= =E5=A5=8B"""
    result = quopri.decodestring(text).decode("u8")
    print(result)


def format_Date(input_date):
    """格式化日期"""
    datetime_str = input_date.split(' ')[1:6]  # 提取日期时间部分
    formatted_datetime = ' '.join(datetime_str)
    return pd.to_datetime(formatted_datetime).strftime("%Y-%m-%d %H:%M:%S")


if __name__ == '__main__':
    email_163 = Email(imap=IMAP_SERVER, account=ACCOUNT, password=PASSWORD, file_save_path=FILE_SAVE_PATH)
    print(email_163.get_newest())
