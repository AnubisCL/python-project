import time  # 用于延时
from selenium.webdriver.common.by import By  # 导入By包进行元素定位
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
import sys
URL = sys.argv[1]
#URL = 'https://www.wjx.cn/vm/mtt97OS.aspx#'

print('py:'+URL)

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
    textInput('q1', 'XX')
    textInput('q2', 'XXXXX')
    textInput('q3', 'XXXX')
    SingleSelection("4_1")
    # q5 浙江-杭州市-拱墅区
    # textInput('q5', '浙江-杭州市-拱墅区')
    # selectArea('q5')
    # q6 浙江-杭州市-拱墅区
    # textInput('q6', '浙江-杭州市-拱墅区')
    # selectArea('q6')
    textInput('q7', 'XXX')
    textInput('q8', 'XXX')
    textInput('q9', 'XXX')
    SingleSelection("10_3")
    SingleSelection("11_1")
    SingleSelection("12_1")
    SingleSelection("13_1")
    SingleSelection("14_1")
    SingleSelection("15_1")
    SingleSelection("16_1")
    SingleSelection("17_1")
    SingleSelection("18_1")
    SingleSelection("19_1")
    SingleSelection("20_2")
    SingleSelection("21_2")
    SingleSelection("22_2")
    SingleSelection("23_1")
    SingleSelection("24_3")
    SingleSelection("25_1")
    SingleSelection("26_1")
    SingleSelection("27_1")
    SingleSelection("28_1")
    SingleSelection("29_2")
    SingleSelection("30_2")
    SingleSelection("31_2")
    textInput('q32', '无')

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
    value = '浙江-杭州市-余杭区'
    ques5 = browser.find_element(by=By.ID, value=id)
    print(ques5.text)
    ques5.send_keys(value)
    print(ques5.text)
    time.sleep(0.5)

    # select2-province-ua-container
    # browser.find_element(by=By.CLASS_NAME, value='layer_content').find_element().click()
    # time.sleep(0.1)

    # 获取select页面元素对象
    # province = browser.find_element(by=By.CLASS_NAME, value='select2-selection__rendered')
    # province.text = "浙江"
    # province.accessible_name = "浙江"
    # time.sleep(0.5)

    # browser.find_element(by=By.CLASS_NAME, value='select2-selection__rendered')
    # city = Select(browser.find_element(by=By.ID, value='city'))
    # area = Select(browser.find_element(by=By.ID, value='area'))


    # city.select_by_value("杭州市")
    # time.sleep(0.1)
    # area.select_by_value("余杭区")
    # time.sleep(0.1)
    #
    # browser.find_element(by=By.CLASS_NAME, value="save_btn").click()
    # time.sleep(0.5)

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
