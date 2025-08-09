import os
from urllib.parse import quote

import ddddocr
from DrissionPage import WebPage
from DrissionPage._pages.chromium_page import ChromiumPage
from PIL import Image, ImageEnhance, UnidentifiedImageError


class Config:
    base_url = ""
    keywords = "JOJO"

    def __init__(self):
        self.base_url = "https://vidhub.tv/"


# 搜索操作
def search(base_url):
    # 默认d模式创建对象
    page = WebPage()
    page.get(base_url)
    page.set.auto_handle_alert()  # 自动处理提示框，使提示框不会弹窗而直接被处理掉

    # 我知道了
    # page.actions.move_to('//div[@class="popup-footer"]/span').click()
    page.ele('xpath://input[@id="txtKeywords"]').input(Config.keywords)

    page.remove_ele('xpath://divz[@id="dZfQis"]')
    page.remove_ele('xpath://div[@id="dZfQis"]')

    # 验证码 https://vidhub.tv/verify/index.html
    page.listen.start('verify/index.html')
    page.ele('xpath://button[@type="submit"]').click()
    res_code = page.listen.wait()
    print(res_code.url)
    txt_code = getTxtCode(res_code.response.body)
    page.ele('xpath://input[@placeholder="请输入上图验证码"]').input(txt_code)
    page.ele('xpath://input[@value="提交"]').click()


# 获取验证码
def getTxtCode(res):
    with open('code.jpg', 'wb') as f:
        f.write(res)
    img_path = os.path.abspath(".") + '/code.jpg'
    process_img_path = process_img(img_path)
    ocr = ddddocr.DdddOcr()
    with open(process_img_path, 'rb') as f:
        img_bytes = f.read()
    text = ocr.classification(img_bytes)
    return text


# 图像处理
def process_img(img_path):
    try:
        # 读取图片并进行灰度处理和二值化
        img = Image.open(img_path).convert('L')  # 灰度处理
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(2)  # 增加对比度
        threshold = 140  # 设定阈值
        img = img.point(lambda p: p > threshold and 255)  # 二值化
        img.save('processed_code.jpg')
        return os.path.abspath(".") + '/processed_code.jpg'
    except (FileNotFoundError, UnidentifiedImageError) as e:
        print("Error processing image:", e)
        return None


#  验证码识别
def machineVerification(page):
    res_code = page.listen.wait()
    txt_code = getTxtCode(res_code.response.body)
    print('验证码为：' + txt_code)
    page.ele('xpath://input[@placeholder="请输入上图验证码"]').input(txt_code)
    page.ele('xpath://input[@value="提交"]').click()


if __name__ == '__main__1':
    search(Config().base_url)

# 网站搜素信息
if __name__ == '__main__':
    key_words = 'JOJO'
    encoded_text = quote(key_words, 'utf-8')
    page_url = 'https://vidhub.tv/vodsearch/' + encoded_text + '-------------.html'
    page = WebPage()
    # page.set.blocked_urls('*.css*')  # 设置不加载css文件

    page.listen.start('verify/index.html')
    page.get(page_url)

    h1_ele = page.s_ele('xpath://h1')
    if not h1_ele:
        print('需要人机验证==>')
        machineVerification(page)
        h1_ele = page.s_ele('xpath://h1')
        while not h1_ele:
            print('人机验证失败，重试==>')
            machineVerification(page)
            h1_ele = page.s_ele('xpath://h1')
    else:
        print('不需要人机验证==>')
        page.listen.stop()

    # TODO 查看结果集是否需要点击下一页

    # 不加载广告
    page.remove_ele('xpath://divz[@id="dZfQis"]')
    page.remove_ele('xpath://div[@id="dZfQis"]')

    # 封面
    img_src = page.ele('xpath://div[@class="module-items"]/div[1]/div[@class="video-cover"]/div/div/img').link
    a_link = page.ele('xpath://div[@class="module-items"]/div[1]/div[@class="video-cover"]/div/div/a').link
    is_completed = page.ele(
        'xpath://div[@class="module-items"]/div[1]/div[@class="video-info"]/div[@class="video-info-header"]/a').text
    a_title = page.ele(
        'xpath://div[@class="module-items"]/div[1]/div[@class="video-info"]/div[@class="video-info-header"]/h3/a').text
    a_type = page.ele(
        'xpath://div[@class="module-items"]/div[1]/div[@class="video-info"]/div[@class="video-info-header"]/div/a').text
    i_year = page.ele(
        'xpath://div[@class="module-items"]/div[1]/div[@class="video-info"]/div[@class="video-info-header"]/div/div[1]').text
    i_country = page.ele(
        'xpath://div[@class="module-items"]/div[1]/div[@class="video-info"]/div[@class="video-info-header"]/div/div[2]').text
    i_daoyan = page.ele(
        'xpath://div[@class="module-items"]/div[1]/div[@class="video-info"]/div[@class="video-info-main"]/div[1]').text
    i_zhuyan = page.ele(
        'xpath://div[@class="module-items"]/div[1]/div[@class="video-info"]/div[@class="video-info-main"]/div[2]').text
    i_desc = page.ele(
        'xpath://div[@class="module-items"]/div[1]/div[@class="video-info"]/div[@class="video-info-main"]/div[3]').text

    print(
        f'{a_link} - {is_completed} - {a_title} - {a_type} - {i_year} - {i_country} - {i_daoyan} - {i_zhuyan} - {i_desc}')

    # 强制关闭
    page.stop_loading()

# 滑块测试
if __name__ == '__main__3':
    page = ChromiumPage()
    page.get("https://auth.smartedu.cn/uias/login")
    page('.m_slider thumb').drag(241)
    page.stop_loading()
