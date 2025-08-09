#!/usr/bin/env python
import sys

import ddddocr
from DrissionPage._configs.chromium_options import ChromiumOptions
from DrissionPage._functions.web import get_blob
from DrissionPage._pages.web_page import WebPage


class Account:
    def __init__(self, id, name, password):
        self.id = id
        self.name = name
        self.password = password

    def showinfo(self):
        return self.id + "," + self.name + "," + self.password


def login(page, account):
    tab = page.new_tab(url="https://xxx.xxx.x.xxx")

    tab.ele('xpath://form/div[1]/input').input(account.id)
    tab.ele('xpath://form/div[2]/input').input(account.password)
    tab.ele('xpath://button[@type="submit"]').click()
    tab.ele('xpath://div[@class="tab flex-h"]/div[1]').click()
    # 验证码
    # tab.ele('xpath://div[@class="input-icon"]/input').input("123456")
    tab.listen.start(targets='blob:', method='GET')  # 开启监听验证码请求抓包
    tab.ele('xpath://div[@class="setCode imgWrapper"]/img').click()  # 点击刷新验证码
    res_code = tab.listen.wait()    # 抓取验证码blob请求
    blobByte = get_blob(tab, res_code.url)  # dp库的获取blob方法获取图片二进制字节
    # img = Image.open(BytesIO(blobByte))  # 使用PIL库打开图片
    # img.show()  # 显示图片
    ocr = ddddocr.DdddOcr()
    code = ocr.classification(blobByte)     # 调用验证码识别
    tab.listen.stop()   # 关闭监听
    tab.ele('xpath://div[@class="input-icon"]/input').input(code)
    tab.ele('xpath://div[@class="submitBtn"]/button').click()


if __name__ == '__main__':
    co = ChromiumOptions().set_browser_path(r"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
    co.ignore_certificate_errors()  # 不校验证书
    page = WebPage(chromium_options=co)
    page.wait.load_start()
    accounts = [
        Account("19*******60", "XX", "XXXX"),
    ]

    if len(sys.argv) > 1:
        index = int(sys.argv[1])
        print("Account:", accounts[index].showinfo())
        login(page, accounts[index])
    else:
        login(page, accounts[0])
        print("Account:", accounts[0].showinfo())
    page.stop_loading()
