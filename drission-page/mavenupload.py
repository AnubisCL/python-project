from DrissionPage import ChromiumPage
from DrissionPage import WebPage
from DrissionPage import SessionPage
from DrissionPage.common import ActionChains
from DrissionPage import ChromiumPage



def loginNexus():
    # 创建页面对象，并启动或接管浏览器
    page = ChromiumPage()
    page.set.load_strategy.eager()
    ac = ActionChains(page)
    # 跳转到登录页面
    page.get('http://127.0.0.1:8081/index.html')
    # 定位到账号文本框，获取文本框元素
    sign = page('xpath//*[@id="nx-header-signin-1144"]')
    ac.move_to(ele_or_loc=sign).click()

    # 定位到密码文本框并输入密码
    page.ele('#usernamefield').input('paydev')
    page.ele('#passwordfield').input('pavdev#996')
    # 点击登录按钮
    page.ele('#button-1170-btnIconEl').click()
    # 点击DEV


if __name__ == '__main__':
    loginNacos()