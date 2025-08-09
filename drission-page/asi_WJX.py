import time  # 用于延时
from selenium.webdriver.common.by import By  # 导入By包进行元素定位
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
import sys
# 启动 python asi_WJX.py

URL = sys.argv[1]
print(URL)

# 实例化一个启动参数对象
chrome_options = Options()

# 添加启动参数
# 添加请求头
chrome_options.add_argument('user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"')
chrome_options.add_argument('--disable-blink-features=AutomationControlled')

# 设置开发者模式启动
chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])

# 关闭selenium对chrome driver的自动控制
chrome_options.add_experimental_option('useAutomationExtension', False)

# 设置驱动程序，启动浏览器  （实现以特定参数启动）
browser = webdriver.Chrome(options=chrome_options)

# 用来执行Chrome开发这个工具命令
browser.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'})

# 获取问卷信息(此处填问卷链接)
browser.get(URL)

def run():
    textInput('q1', 'XXX')
    textInput('q2', 'XXX')
    textInput('q3', 'XXX')
    SingleSelection("4_1")
    SingleSelection("5_1")
    # q6 暂时不生效
    textInput('q6', 'XXX')
    # selectArea('q6')
    # q7 暂时不生效
    textInput('q7', 'XXX')
    # selectArea('q7')
    textInput('q8', 'XXX')
    textInput('q9', 'XXX')
    textInput('q10', 'XXX')
    SingleSelection("11_1")
    SingleSelection("12_1")
    SingleSelection("13_1")
    SingleSelection("14_1")
    SingleSelection("15_1")
    SingleSelection("16_3")
    SingleSelection("17_1")
    SingleSelection("18_1")
    SingleSelection("19_1")
    SingleSelection("20_1")
    SingleSelection("21_2")
    SingleSelection("22_2")
    SingleSelection("23_2")
    SingleSelection("24_1")
    SingleSelection("25_4")
    SingleSelection("26_1")
    SingleSelection("27_1")
    SingleSelection("28_1")
    SingleSelection("29_1")
    SingleSelection("30_2")
    SingleSelection("31_2")
    SingleSelection("32_2")
    textInput('q33', '无')

    # 点击提交
    # submit = browser.find_element_by_xpath("//*[@id='ctlNext']")  # 网页源代码的xpath: //*[@id="ctlNext"]
    submit = browser.find_element(by=By.XPATH, value="//*[@id='ctlNext']")  # 网页源代码的xpath: //*[@id="ctlNext"]
    submit.click()  # 点击
    # 延时 太快会被检测是脚本
    time.sleep(0.3)

    # 模拟点击智能验证按钮
    # 先点确认
    browser.find_element(By.XPATH, "//button[text()='确认']").click()
    time.sleep(1)
    # 再点智能验证提示框，进行智能验证
    browser.find_element_by_xpath("//div[@id='captcha']").click()

# 下拉框
def selectArea(id):
    browser.find_element(by=By.ID, value=id).click()
    time.sleep(0.1)
    # 获取select页面元素对象；
    province = Select(browser.find_element(by=By.ID, value='province'))
    city = Select(browser.find_element(by=By.ID, value='city'))
    area = Select(browser.find_element(by=By.ID, value='area'))

    province.select_by_value("浙江")
    time.sleep(0.1)
    city.select_by_value("杭州市")
    time.sleep(0.1)
    area.select_by_value("拱墅区")
    time.sleep(0.1)

    browser.find_element(by=By.CLASS_NAME, value="save_btn").click()
    time.sleep(0.5)

# 文本输入框
def textInput(id, value):
    browser.find_element(by=By.ID, value=id).send_keys(value)
    time.sleep(0.1)

# 单项选择 7-1 表示 第七题 第一项
def SingleSelection(item):
    js = "document.getElementById(\"q" + item + "\").parentElement.click()"
    browser.execute_script(js)
    time.sleep(0.1)

# 多项选择
def MultiSelecttion(items):
    # TODO 待添加
    time.sleep(0.1)

if __name__ == "__main__":
    # 批量提交问卷
    run()
