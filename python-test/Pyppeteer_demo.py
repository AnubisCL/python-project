'''
Description: 问卷星自动表单提交 pyppeteer
'''
import asyncio
from pyppeteer import launch
from pyppeteer_stealth import stealth  # 反爬虫第三方库
import time  # 用于延时
import sys

# 接受外部参数
# URL = sys.argv[1]
# print('py:'+URL)
URL = 'http://'

async def main():
    browser = await launch({
        #配置浏览器地址
        'executablePath': 'C:/Users/17902/AppData/Local/Google/Chrome/Application/chrome.exe',
        # 'executablePath': 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',
        # 'executablePath': 'C:\Program Files\Internet Explorer/iexplore.exe',
        # Pyppeteer 默认使用的是无头浏览器,所以要显示需要给False
        'headless': False,
        'args': ['--no-sandbox', '--window-size=1366,850']
    })

    page = await browser.newPage()
    page2 = await browser.newPage()
    page3 = await browser.newPage()
    page4 = await browser.newPage()
    await page.setViewport({'width': 1366, 'height': 768})
    # 防止页面识别出脚本(反爬虫关键语句)
    await stealth(page)
    url = URL
    await page.goto(url)
    # input框：page.type(selector,text),在指定selector的元素上填写text
    await page.type('#q1', '')  # CssSelector
    await page.xpath('','')    # xpath

    # Radio 单选框：先用page.querySelector(selector)找到指定的元素,再调用元素的click()方法、还可以用xpath方法
    # CssSelector: ul在第二个次序、li在第二个次序、a标签在第二个次序
    button = await page.querySelector('#div4 > div:nth-child(2) > div:nth-child(1) > span > a')
    await button.click()

    # 下拉框：div层级选择模拟选择
    # q5
    address = await page.querySelector("#q5")
    await address.click()
    time.sleep(0.5)
    province = await page.querySelector("#divFrameData > div.layer_content > div:nth-child(2) > div > span > span:nth-child(1) > span > span:nth-child(2) > b")
    await province.click()
    provinceOption = await page.querySelector("span.select2-results > ul > li:nth-child(12)")
    await provinceOption.click()
    city = await page.querySelector("#divFrameData > div.layer_content > div:nth-child(3) > div > span > span:nth-child(1) > span > span:nth-child(2) > b")
    await city.click()
    cityOption = await page.querySelector("span.select2-results > ul > li:nth-child(2)")
    await cityOption.click()
    area = await page.querySelector("#divFrameData > div.layer_content > div:nth-child(4) > div > span > span:nth-child(1) > span > span:nth-child(2) > b")
    await area.click()
    areaOption = await page.querySelector("span.select2-results > ul > li:nth-child(7)")
    await areaOption.click()
    finishSubmit = await page.querySelector("#divFrameData > div.layer_content > div:nth-child(5) > a")
    await finishSubmit.click()

    # # 日期选择题：先点击日期选择框,在出现的iframe寻找元素并调用click()方法
    # date1 = await page.querySelector("#q4")
    # await date1.click()
    # frame = page.frames
    # date2 = await frame[1].querySelector('#selectTodayButton')
    # await date2.click()

    # 找到提交按钮提交
    submit = await page.querySelector('#ctlNext')
    await submit.click()
    await asyncio.sleep(2)
    await browser.close()   # 关闭浏览器

asyncio.get_event_loop().run_until_complete(main())

if __name__ == "__main__":
    # 批量提交问卷
    main()

# # 反爬虫：原理是将get请求转换成undefined, 也可以用stealth库来防止机器人检测
# await stealth(page)
# await page.evaluateOnNewDocument('Object.defineProperty(navigator, "webdriver", {get: () => undefined})')
#
# # 三种解析方式
# Page.querySelector()           # CSS选择器
# Page.querySelectorAll()
# Page.xpath()                   # xpath
# page.evaluate('window.scrollBy(0, window.innerHeight)') # 执行js语句
# # Pyppeteer的evaluate()方法只使用JavaScript字符串，该字符串可以是函数或表达式。可以添加选项force_expr=True，强制Pyppeteer作为表达式处理。
