from DrissionPage import ChromiumPage


def loginNacos():
    # 创建页面对象，并启动或接管浏览器
    page = ChromiumPage()
    ac = ActionChains(page)
    # 跳转到登录页面
    page.get('http://127.0.0.1:13068/nacos/index.html#/login')
    # 定位到账号文本框，获取文本框元素
    page.ele('#username').input('nacos')
    # 定位到密码文本框并输入密码
    page.ele('#password').input('nacos')
    # 点击登录按钮
    page.ele('xpath://*[@id="root"]/div/section/div[7]/div/div/form/div[3]/div[2]/button').click()
    # 点击DEV
    page.ele('xpath://*[@id="root"]/div/div[2]/div/div/div[1]/div/div/div[2]/div/div/div/div[2]/span[2]').click()


if __name__ == '__main__':
    loginNacos()