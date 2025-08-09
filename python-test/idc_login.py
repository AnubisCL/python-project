'''
Description:
'''
import asyncio  # asyncio是Python的一个异步协程库，自3.4版本引入的标准库，直接内置了对异步IO的支持
from pyppeteer import launch
from pyppeteer_stealth import stealth  # 反爬虫第三方库

async def main():
    browser = await launch({
        #配置浏览器地址
        'executablePath': 'C:/Program Files/Google/Chrome/Application/chrome.exe',
        # 'executablePath': 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',
        # Pyppeteer 默认使用的是无头浏览器,所以要显示需要给False
        # 是否显示浏览器窗口
        'headless': False,
        #'devtools': False,  打开F12控制台
    'args': ['--no-sandbox', '--window-size=1366,850']
    })

    page = await browser.newPage()
    await page.setViewport({'width': 1366, 'height': 768})
    # 防止页面识别出脚本(反爬虫关键语句)
    await stealth(page)
    await page.goto('http://XXXXXX/login')
    # 1.账号密码
    await page.type('input[type="text"]', '18785234121')
    await page.type('input[type="password"]', '123456')
    # 1.5 验证码
    checkCode = await page.querySelector('div[class="login-code"]')

    # 2.记住密码
    check = await page.querySelector('div.login > form > label > span:nth-child(1) > span')
    await check.click()
    # 3.登录
    await page.click('button[type="button"]')
    # 等待元素出现
    await page.waitForSelector('#topmenu-container', {'visible': 'true'})
    # 4.工单管理
    await page.click('#topmenu-container > li.el-menu-item:nth-child(4)')
    await page.waitForSelector('#hamburger-container', {'visible': 'true'})
    # 5.工单创建新
    await page.click('#app > div > div > div.content-container > div.side-bar-ai.sidebar-container.has-logo > div.el-scrollbar.theme-dark > div.scrollbar-wrapper.el-scrollbar__wrap > div > ul > div:nth-child(4) > a > li')

    # 获取当前页cookie
    # cookies = await page.cookies()
    # print(cookies)
    # evaluate()是执行js的方法，js逆向时如果需要在浏览器环境下执行js代码的话可以利用这个方法
    # js为设置webdriver的值，防止网站检测
    # await page.evaluate('''() =>{ Object.defineProperties(navigator,{ webdriver:{ get: () => false } }) }''')

    # await page.screenshot({'path': './screenshot.jpg'})   # 截图保存路径

    # page_text = await page.content()  # 获取网页源码
    # print(page_text)

    await page.close()   # 关闭页面
    await browser.close()   # 关闭浏览器




if __name__ == "__main__":
    # 批量提交问卷
    asyncio.get_event_loop().run_until_complete(main())


# # 反爬虫：原理是将get请求转换成undefined, 也可以用stealth库来防止机器人检测
# await stealth(page)
# await page.evaluateOnNewDocument('Object.defineProperty(navigator, "webdriver", {get: () => undefined})')

# 在页面内执行 document.querySelector。如果没有元素匹配指定选择器，返回值是 None
# J = querySelector
# 在页面内执行 document.querySelector，然后把匹配到的元素作为第一个参数传给 pageFunction
# Jeval = querySelectorEval
# 在页面内执行 document.querySelectorAll。如果没有元素匹配指定选择器，返回值是 []
# JJ = querySelectorAll
# 在页面内执行 Array.from(document.querySelectorAll(selector))，然后把匹配到的元素数组作为第一个参数传给 pageFunction
# JJeval = querySelectorAllEval
# XPath表达式
# Jx = xpath

