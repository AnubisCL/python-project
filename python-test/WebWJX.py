import random          # 用于产生随机数
import time            # 用于延时

from adodbapi.examples.xls_read import driver
from selenium.webdriver.common.by import By      #导入By包进行元素定位
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# 实例化一个启动参数对象
chrome_options = Options()

# 添加启动参数
# 添加请求头
chrome_options.add_argument(
    'user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"')
chrome_options.add_argument('--disable-blink-features=AutomationControlled')

# 防止被识别
# 设置开发者模式启动
chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])

# 关闭selenium对chrome driver的自动控制
chrome_options.add_experimental_option('useAutomationExtension', False)
# 网页最大化
# chrome_options.maximize_window()

#设置浏览器以无界面方式运行
# chrome_options.add_argument('headless')

#设置驱动程序，启动浏览器  （实现以特定参数启动）
browser = webdriver.Chrome(options=chrome_options)

#用来执行Chrome开发这个工具命令
browser.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument',
                        {'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'})


# driver.get('https://www.wjx.cn/vm/wT0xLos.aspx')    # 亚信问卷星
driver.get('https://www.wjx.cn/vm/wT0xLos.aspx')



# ======================== 单选题 ======================
# 问题1的点击 （姓名）
randomId = random.randint(1, 2)  # 随机点击第一个选项或第二个选项
# js实现方式
js = "document.getElementById(\"q1_" + str(randomId) + "\").checked = true"
browser.execute_script(js)  # 使用js实现点击的效果（调用js方法，同时执行javascript脚本）
js = "document.getElementById(\"q1_" + str(randomId) + "\").click()"
browser.execute_script(js)  # 使用js实现点击的效果（调用js方法，同时执行javascript脚本）
# 延时 太快会被检测是脚本
time.sleep(1)

# 问题2    （年龄）
randomId = random.randint(2, 4)  # 随机数，5个多选框 随机点击
# js实现方式
js = "document.getElementById(\"q2_" + str(randomId) + "\").checked = true"
browser.execute_script(js)
js = "document.getElementById(\"q2_" + str(randomId) + "\").click()"  # 拼接字符串的方式 js找到对应id 点击按钮
browser.execute_script(js)
# 延时
time.sleep(0.1)
# =====================================================
# ======================== 多选题 ======================
# 问题5
randomId = random.randint(1, 3)  # 随机数选择（选多少个）
for i in range(1, randomId + 1):  # 循环 实现多选效果
    randomId1 = random.randint(1, 6)  # 随机选择第1到第6个选项之一
    # 两种js实现方式
    js = "document.getElementById(\"q5_" + str(randomId1) + "\").checked = true"
    browser.execute_script(js)
    js = "document.getElementById(\"q5_" + str(randomId1) + "\").click()"
    browser.execute_script(js)
# 延时
time.sleep(1)
# =====================================================
# ======================== 填空题 ======================
# 问题25
# 自定义要填的内容
block = ["定义第1个填空", "定义第2个填空", "定义第3个填空", "定义第4个填空", "定义第5个填空", "定义第6个填空", "无"]
# 在上述内容中随机选择一个填入
randomId = random.randint(0, 5)  # （数值下标从0开始）
# 在题目中随机输入上述内容
browser.find_element_by_id("q25").send_keys(block[randomId])
# 延时
time.sleep(0.1)