from DrissionPage._configs.chromium_options import ChromiumOptions
from DrissionPage._pages.web_page import WebPage

# 1.获取视频链接，图片，info链接
def step_1():
    # 创建页面对象
    # co = ChromiumOptions().set_browser_path(r"/usr/share/applications/chromium-browser.desktop")
    co = ChromiumOptions().set_browser_path(r"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
    co.incognito()  # 匿名模式
    co.headless(True)   # 无头模式
    co.set_argument('--no-sandbox')
    co.ignore_certificate_errors()  # 不校验证书
    page = WebPage(chromium_options=co)
    page.set.load_mode.eager()
    for i in range(1, 2):  # 共 26（24年11月19日）页
        page.get('https://b9bda2dc56dc698a8cc361dc77f81387.81tvs6.top/vod/type/id/27/page/' + str(i) + '.html')
        # 在页面中查找元素
        items = page.eles('xpath://li/div')
        # 遍历元素
        for item in items[:-1]:
            video_title = item.ele("xpath://div/h4/a").title
            video_box = item.ele("xpath://a")
            videoLink = video_box.attrs['href']
            imageUrl = video_box.attrs['title']

            # 打印<a>元素文本和href属性
            if '/vod/play/id/' in videoLink and '糖心' in video_title:
                print(video_title + '|' + videoLink + '|' + imageUrl) # 粘贴到tx-info.txt
        page.wait.load_start()

# 2.读取文件 ,获取m3u8地址
def step_2():
    BASE_URL = 'https://b9bda2dc56dc698a8cc361dc77f81387.81tvs6.top'
    co = ChromiumOptions().set_browser_path(r"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
    co.incognito()  # 匿名模式
    co.headless(True)  # 无头模式
    co.set_argument('--no-sandbox')
    co.ignore_certificate_errors()  # 不校验证书

    # 文件路径
    file_path = '/Users/anubis/Downloads/video-hls/tx-info.txt'
    print()
    # 使用with语句打开文件，确保文件在操作完成后能够正确关闭
    with open(file_path, 'r', encoding='utf-8') as file:
        # 使用for循环逐行读取文件
        for line in file:
            page = WebPage(chromium_options=co)
            page.set.load_mode.none()
            page.listen.start(targets='.m3u8', method='GET')  # 开启监听验证码请求抓包
            # 去除每行末尾的换行符
            old_line = line.strip()
            sub_url = old_line.split('|')[1]
            page.get(BASE_URL + sub_url)
            m3u8 = page.listen.wait()  # 抓取m3u8请求
            m3u8_url = m3u8.url
            page.stop_loading()
            page.close_tabs()
            print(old_line + "|" + m3u8_url)    # 粘贴到tx-m3u8.txt

if __name__ == '__main__':
    step_1()
    # step_2()