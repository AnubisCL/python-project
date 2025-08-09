# -*- coding: utf-8 -*-
# @Desc    : Win GUI，自动获取验证码，自动读取邮箱
# @Time    : 2024/02/27 15:10
# @Author  : Anubis
from datetime import datetime
from email.header import decode_header
import os
import email
import imaplib
import quopri
import re
import time
import socket
import pandas as pd
import subprocess
import uiautomation as auto
import logging
from logging import handlers

# 设置句柄全局搜索超时配置(秒)
auto.uiautomation.SetGlobalSearchTimeout(15)
# 邮箱配置
IMAP_SERVER = 'imap.163.com'
ACCOUNT = ''    # 邮箱账号
PASSWORD = ''   # 邮箱 POP3/SMTP 授权码
FILE_SAVE_PATH = r''
# ATrust 配置
ATRUST_EMAIL_TYPE = 'ATrust-验证码'
ATRUST_PATH = 'C:\\Program Files (x86)\\Sangfor\\aTrust\\aTrustTray\\aTrustTray.exe'
ATRUST_ACCOUNT = '' # ATrust 账户
ATRUST_PASSWORD = '' # ATrust 密码
# FFCS_SOM 配置
FFCS_WINDOW_NAME = 'FFCS_SOM 1.2.1_2'
FFCS_EMAIL_TYPE = 'FFCS-验证码'
FFCS_PATH = 'C:\\FFCS_SOM\\FFCS_som.exe'
FFCS_ACCOUNT = ''
FFCS_PROXY_IP = ''
FFCS_PROXY_PORT = ''
FFCS_PASSWORD = '' # 堡垒密码
# socket5 代理配置
SOCKET_CONFIG_PATH = 'C:\\nvm\\v6.14.4\\node_modules\\shadowsocks\\config.json'
SOCKET_SERVER_PORT = '8388'


class Logger(object):
    level_relations = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'crit': logging.CRITICAL
    }  # 日志级别关系映射

    def __init__(self, filename, level='info', when='D', backCount=3,
                 fmt='%(asctime)s - [line:%(lineno)d] - %(levelname)s: %(message)s'):
        self.logger = logging.getLogger(filename)
        format_str = logging.Formatter(fmt)  # 设置日志格式
        self.logger.setLevel(self.level_relations.get(level))  # 设置日志级别
        sh = logging.StreamHandler()  # 往屏幕上输出
        sh.setFormatter(format_str)  # 设置屏幕上显示的格式
        th = handlers.TimedRotatingFileHandler(filename=filename, when=when, backupCount=backCount,
                                               encoding='utf-8')  # 往文件里写入#指定间隔时间自动生成文件的处理器
        # 实例化TimedRotatingFileHandler
        # interval是时间间隔，backupCount是备份文件的个数，如果超过这个个数，就会自动删除，when是间隔的时间单位，单位有以下几种：
        # S 秒
        # M 分
        # H 小时、
        # D 天、
        # W 每星期（interval==0时代表星期一）
        # midnight 每天凌晨
        th.setFormatter(format_str)  # 设置文件里写入的格式
        self.logger.addHandler(sh)  # 把对象加到logger里
        self.logger.addHandler(th)


log = Logger('atrust_ffcs_start_all.log', level='debug')


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

    def get_newest(self):
        """获取最新的未读邮件,自动下载附件"""
        for msg_data in self.check_email(message_type=self.Unseen):
            log.logger.debug(u"邮件主题：{subject}\n邮件日期：{date}\n附件列表：{files}\n邮件正文：{content}".format(
                subject=msg_data.get('subject'),
                date=msg_data.get('date'),
                files=msg_data.get('files'),
                content=msg_data.get('content')
            ))
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
            log.logger.debug(info)
            raise StopIteration
        # 选择邮件类型
        search_status, items = self.imap_server.search(None, message_type)
        if select_status != 'OK':
            log.logger.debug(items)
            raise StopIteration
        message_list = items[0].split()[-1:] if last_message else items[0].split()[:count]
        log.logger.info("阅读最近30天内的邮,类型【{}】,共【{}】条, 读取【{}】条".format(message_type, len(items[0].split()),
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
                    log.logger.debug('Attachment : ' + file_name)
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

    def get_email_by_subject(self, email_type, send_date):
        """获取指定的未读邮件,自动下载附件"""
        result_email = {}
        email_list = self.check_email(last_message=False, message_type=self.Unseen, count=10)
        for msg_data in email_list:
            log.logger.info(u"\n邮件主题：{subject}\n邮件日期：{date}\n附件列表：{files}\n邮件正文：{content}".format(
                subject=msg_data.get('subject'),
                date=msg_data.get('date'),
                files=msg_data.get('files'),
                content=msg_data.get('content')
            ))
            if email_type == msg_data.get('subject') and send_date < msg_data.get('date'):
                result_email = msg_data
                break
        return result_email


def decode_MIME():
    """MIME字符进行解码"""
    text = """=E5=9B=A0=E4=B8=BA=E4=B8=81=E4=BF=8A=E6=99=96=E5=8F=AA=E8=B7=9F=E7=9D=80= =E9=BA=A6=E8=BF=AA=E5=B0=B1=E4=B8=8D=E5=8F=AF=E8=83=BD=E9=82=A3=E5=88=B0= =E6=80=BB=E5=86=A0=E5=86=9B=E6=88=92=E6=8C=87=EF=BC=8C=E8=80=83=E8=99=91= =E5=88=B0=E6=8A=A4=E7=90=83=E9=97=AE=E9=A2=98=EF=BC=8C=E5=A6=82=E6=9E=9C= =E7=94=A8=E9=BA=A6=E8=BF=AA=E6=8D=A2=E4=BA=A8=E5=88=A9=E7=9A=84=E8=AF=9D= =E8=AF=B4=E4=B8=8D=E5=AE=9A=E5=B0=B1=E8=A1=8C=EF=BC=8C=E5=BD=93=E7=84=B6= =E8=AF=B8=E8=91=9B=E5=AD=94=E6=98=8E=E8=BF=99=E4=B8=AA=E8=80=81=E7=8B=90= =E7=8B=B8=E8=82=AF=E5=AE=9A=E6=98=AF=E7=95=A5=E6=87=82=E8=BF=99=E4=BB=B6= =E4=BA=8B=E7=9A=84=EF=BC=8C=E4=BB=96=E7=AC=AC=E4=B8=80=E4=B8=AA=E4=B8=8D= =E7=AD=94=E5=BA=94=EF=BC=8C=E5=B0=B1=E7=AE=97=E4=BB=96=E7=AD=94=E5=BA=94= =E4=BA=86=EF=BC=8C=E7=BC=9D=E5=B0=8F=E8=82=9B=E8=83=BD=E7=AD=94=E5=BA=94= =E5=90=97=EF=BC=9F=E6=89=80=E4=BB=A5=E8=BF=99=E6=95=B4=E4=BB=B6=E4=BA=8B= =E6=83=85=E7=9A=84=E4=BA=AE=E7=82=B9=E5=B0=B1=E5=9C=A8=E4=BA=8E=E7=A7=A6= =E5=A5=8B"""
    result = quopri.decodestring(text).decode("u8")
    log.logger.debug(result)


def format_Date(input_date):
    """格式化日期"""
    datetime_str = input_date.split(' ')[1:6]  # 提取日期时间部分
    formatted_datetime = ' '.join(datetime_str)
    return pd.to_datetime(formatted_datetime).strftime("%Y-%m-%d %H:%M:%S")


def match_ATrust_Code(content):
    """匹配 验证码"""
    match = re.search(r"验证码为:(\d+)", content)
    if match:
        verification_code = match.group(1)
        return verification_code
    else:
        return None


def match_FFCS_Code(content):
    """匹配 验证码"""
    match = re.search(r"短信口令为(\d+)", content)
    if match:
        verification_code = match.group(1)
        return verification_code
    else:
        return None


def get_verification_code(email_type, send_date, retry=3):
    """获取验证码"""
    try:
        time.sleep(15)
        verification_code = None
        email_163 = Email(imap=IMAP_SERVER, account=ACCOUNT, password=PASSWORD, file_save_path=FILE_SAVE_PATH)
        email_code = email_163.get_email_by_subject(email_type, send_date)
        if ATRUST_EMAIL_TYPE == email_type:
            verification_code = match_ATrust_Code(email_code["content"])
        elif FFCS_EMAIL_TYPE == email_type:
            verification_code = match_FFCS_Code(email_code["content"])
        else:
            log.logger.warning("未匹配到邮件类型：%s", email_type)
        log.logger.info("验证码为：" + verification_code)
        return verification_code  # 将获取到的验证码直接返回
    except KeyError:
        if retry > 0:
            log.logger.warning("未获取到验证码，重试中【%d】...", retry)
            time.sleep(retry * 20)  # 等待时间递减
            return get_verification_code(email_type, send_date, retry - 1)
        else:
            log.logger.error("重试次数已用完，无法获取验证码")
            return None
    except Exception as e:
        log.logger.error(f"发生异常: {e}")


def start_ATrust():
    log.logger.info("启动")
    subprocess.Popen(ATRUST_PATH).wait()
    time.sleep(30)  # 启动大概用时
    aTrust_window = auto.PaneControl(searchDepth=1, Name='aTrust')
    log.logger.info("启动成功")
    try:
        aTrust_window.CustomControl(searchDepth=5, Name='工作台').Click()
        account = aTrust_window.EditControl(searchDepth=23, Name='请输入账号')
        account.GetValuePattern().SetValue(ATRUST_ACCOUNT)
        password = aTrust_window.EditControl(searchDepth=23, Name='请输入登录密码')
        password.GetValuePattern().SetValue(ATRUST_PASSWORD)
        aTrust_window.ButtonControl(searchDepth=19, Name='登录').Click()
    except auto.comtypes.COMError as ex:
        pass
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log.logger.info("获取验证码时间：" + current_time)
    code = get_verification_code(ATRUST_EMAIL_TYPE, current_time)
    try:
        aTrust_window.EditControl(searchDepth=18, Name='').GetValuePattern().SetValue(code)
        aTrust_window.ButtonControl(searchDepth=15, Name='确定').Click()
    except auto.comtypes.COMError as ex:
        pass


def start_FFCS():
    log.logger.info("启动")
    subprocess.Popen(FFCS_PATH)
    ffcs_window = auto.WindowControl(searchDepth=1, Name=FFCS_WINDOW_NAME)
    # ffcs_window.SetTopmost(True)
    log.logger.info(ffcs_window.Name + "启动 成功")

    try:
        # edit.SendKeys('{Ctrl}a{Del}')
        edit = ffcs_window.EditControl()
        edit.GetValuePattern().SetValue(FFCS_ACCOUNT)
        # 高级
        ffcs_window.ButtonControl(searchDepth=2, Name='高级>>').Click()
        ffcs_window.EditControl(searchDepth=2, AutomationId='1007').GetValuePattern().SetValue(
            FFCS_PROXY_IP + ":" + FFCS_PROXY_PORT)
        ffcs_window.EditControl(searchDepth=2, AutomationId='1009').GetValuePattern().SetValue(FFCS_PROXY_IP)
        ffcs_window.EditControl(searchDepth=2, AutomationId='1001').GetValuePattern().SetValue(FFCS_PASSWORD)
        ffcs_window.ButtonControl(searchDepth=2, Name='确定').Click()
    except auto.comtypes.COMError as ex:
        pass
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log.logger.info("获取验证码时间：" + current_time)
    code = get_verification_code(FFCS_EMAIL_TYPE, current_time)
    try:
        ffcs_window_code = auto.WindowControl(searchDepth=1, Name=FFCS_WINDOW_NAME)
        ffcs_window_code.EditControl(searchDepth=2, AutomationId='1000').GetValuePattern().SetValue(code)
        ffcs_window_code.ButtonControl(searchDepth=2, Name='确定').Click()
    except auto.comtypes.COMError as ex:
        pass


def get_local_ip():
    """win 获取本机局域网IP"""
    try:
        host_name = socket.gethostname()
        local_ip = socket.gethostbyname(host_name)
        return local_ip
    except:
        return None


def set_socket5_config():
    """设置 socket5 代理"""
    config_path = SOCKET_CONFIG_PATH
    log.logger.info("自动检查 socket5 配置文件" + config_path)
    ip = get_local_ip()
    if not os.path.exists(config_path):
        log.logger.info("配置文件不存在，创建配置文件")
        with open(config_path, 'w', encoding='utf-8') as f:
            f.write(
                '''
                { 
                    "server":"%s",
                    "server_port":%s,
                    "local_address":"127.0.0.1",
                    "local_port":1080,
                    "password":"barfoo!",
                    "timeout":600,
                    "method":"aes-256-cfb"
                }
                ''' % (ip, SOCKET_SERVER_PORT)
            )
        log.logger.info("配置文件创建成功")
    else:
        log.logger.info("配置文件已存在，修改配置文件中的IP地址为: %s,端口为: %s" % (ip, SOCKET_SERVER_PORT))
        with open(config_path, 'r', encoding='utf-8') as f:
            config_content = f.read()
        new_config_content = re.sub(r'"server"\s*:\s*"\d+\.\d+\.\d+\.\d+"', '"server":"{ip}"'.format(ip=ip),
                                    config_content)
        with open(config_path, 'w', encoding='utf-8') as f:
            f.write(new_config_content)
        log.logger.info("配置文件修改成功")


def start_socket5(taskKill=True, setConfig=False):
    """开启 socket5 代理"""
    # 使用 taskkill 命令终止指定名称的进程
    if taskKill:
        netstat_output = subprocess.run(["netstat", "-ano"], capture_output=True, text=True).stdout
        for line in netstat_output.split('\n'):
            if SOCKET_SERVER_PORT in line and "LISTENING" in line:
                parts = line.split()
                pid = parts[-1]
                subprocess.run(["taskkill", "/F", "/PID", pid])
    if setConfig:
        set_socket5_config()
    # 执行命令打开cmd并运行ssserver
    subprocess.run(["cmd", "/K", "ssserver"], shell=True)


if __name__ == '__main__':
    start_time = datetime.now()
    print(auto.GetRootControl())
    start_ATrust()
    time.sleep(20)
    start_FFCS()
    # start_socket5(setConfig=True)
    end_time = datetime.now()
    log.logger.info("运行时间：%d 秒", (end_time - start_time).seconds)
