from DrissionPage import ChromiumPage
from DrissionPage import WebPage
from DrissionPage import SessionPage


def loginGitee():
    # 创建页面对象，并启动或接管浏览器
    page = ChromiumPage()
    # 跳转到登录页面
    page.get('https://gitee.com/login')
    # 定位到账号文本框，获取文本框元素
    ele = page.ele('#user_login')
    # 输入对文本框输入账号
    ele.input('anubiscl@163.com')
    # 定位到密码文本框并输入密码
    page.ele('#user_password').input('XXX')
    # 点击登录按钮
    page.ele('@value=登 录').click()


def print_hi():
    page = ChromiumPage()
    page.get('http://g1879.gitee.io/DrissionPageDocs')



# 按装订区域中的绿色按钮以运行脚本。
if __name__ == '__main__':
    loginGitee()