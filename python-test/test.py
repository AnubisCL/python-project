import random  # 用于产生随机数
import time  # 用于延时

from selenium.webdriver.common.by import By  # 导入By包进行元素定位
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# 实例化一个启动参数对象
from selenium.webdriver.support.select import Select
# from selenium.webdriver.support.ui import Select
# https://www.wjx.cn/joinnew/setcitycountymobo2.aspx?activityid=176200649&ct=3&pos=6

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

# 设置浏览器以无界面方式运行
# chrome_options.add_argument('headless')

# 设置驱动程序，启动浏览器  （实现以特定参数启动）
browser = webdriver.Chrome(options=chrome_options)

# 用来执行Chrome开发这个工具命令
browser.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument',
                        {'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'})

browser.get('https://www.wjx.cn/joinnew/setcitycountymobo2.aspx?activityid=176200649&ct=3&pos=6')  # 获取问卷信息(此处填问卷链接)


def run():

    # 获取select页面元素对象；
    province = Select(browser.find_element(by=By.ID, value='province'))
    # 获取所有选择项的页面元素对象；
    all_province = province.options  # 打印选项总数；
    print("列表选项总数：", len(all_province))
    # 循环打印出选项序号和对应的选项属性；
    for i in range(len(all_province)):
        print("元素序号：" + str(i))
        print(province.options[i].get_attribute("text"))
        print(province.options[i].get_attribute("value"))  # 通过选项名称"足球"选择内容；
    province.select_by_value("浙江")
    # 打印最后选择选项名称；
    # 等待一下，演示效果；
    time.sleep(3)
    # browser.quit()

    # 获取select页面元素对象；
    city = Select(browser.find_element(by=By.ID, value='city'))
    # 获取所有选择项的页面元素对象；
    all_city = city.options  # 打印选项总数；
    print("列表选项总数：", len(all_city))
    # 循环打印出选项序号和对应的选项属性；
    for i in range(len(all_city)):
        print("元素序号：" + str(i))
        print(city.options[i].get_attribute("text"))
        print(city.options[i].get_attribute("value"))  # 通过选项名称"足球"选择内容；
    city.select_by_value("杭州市")
    # 打印最后选择选项名称；
    # 等待一下，演示效果；
    time.sleep(3)
    # browser.quit() area

    # 获取select页面元素对象；
    area = Select(browser.find_element(by=By.ID, value='area'))
    # 获取所有选择项的页面元素对象；
    all_area = area.options  # 打印选项总数；
    print("列表选项总数：", len(all_area))
    # 循环打印出选项序号和对应的选项属性；
    for i in range(len(all_area)):
        print("元素序号：" + str(i))
        print(area.options[i].get_attribute("text"))
        print(area.options[i].get_attribute("value"))  # 通过选项名称"足球"选择内容；
    area.select_by_value("拱墅区")

    # 打印最后选择选项名称；
    print("最后选择的内容是：", province.all_selected_options[0].text)  # 单选列表所以只能是0；
    print("最后选择的内容是：", city.all_selected_options[0].text)  # 单选列表所以只能是0；
    print("最后选择的内容是：", area.all_selected_options[0].text)  # 单选列表所以只能是0；
    # 等待一下，演示效果；
    time.sleep(3)



    # 获取select页面元素对象；
    # divProvince = Select(browser.find_element(by=By.ID, value='divProvince'))
    # # 获取所有选择项的页面元素对象；
    # all_options = divProvince.options
    #
    # print("列表选项总数：", len(all_options))
    # # 循环打印出选项序号和对应的选项属性；
    # for i in range(len(all_options)):
    #     print("元素序号：" + str(i))
    #     print(divProvince.options[i].get_attribute("text"))
    #     print(divProvince.options[i].get_attribute("value"))  # 通过选项名称"足球"选择内容；
    # divProvince.select_by_value("浙江")
    # # 打印最后选择选项名称；
    # print("最后选择的内容是：", divProvince.all_selected_options[0].text)  # 单选列表所以只能是0；
    # # 等待一下，演示效果；
    # time.sleep(3)


    # browser.find_element(by=By.ID, value='select2-province-container').text('浙江')
    # browser.find_element(by=By.ID, value='select2-city-container').text('杭州市')
    # browser.find_element(by=By.ID, value='select2-area-container').text('拱墅区')

    # browser.find_element(by=By.ID, value='q6').send_keys('浙江-杭州市-拱墅区')
    time.sleep(0.1)

    # q7
    # browser.find_element(by=By.ID, value='q7').send_keys('浙江-杭州市-拱墅区')
    # time.sleep(0.1)

    browser.find_element(by=By.CLASS_NAME, value="save_btn").click()
    time.sleep(0.5)

if __name__ == "__main__":
    # 批量提交问卷
    # for i in range(10):          #运行一次提交10份问卷
    run()
    # time.sleep(5)  # 避免提交过快 会出现验证