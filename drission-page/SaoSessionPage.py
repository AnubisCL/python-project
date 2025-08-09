#!/usr/bin/env python
# -*- coding:utf-8 -*-
# http://g1879.gitee.io/drissionpagedocs/whatsnew/4_0/
# pip install DrissionPage==4.0.0b34
import random
import time

import openpyxl
from DrissionPage import ChromiumOptions
from DrissionPage import ChromiumPage
# 数据类型判断
from DrissionPage.items import ChromiumElement
from colorama import Fore, init
from tabulate import tabulate


# --------------配置类---------------
class Config:
    body = "x:/html/body"
    browser_path = r"C:\Users\Administrator\AppData\Local\Google\Chrome\Application\chrome.exe"
    browser_path2 = r"C:\Program Files\Twinkstar Browser\twinkstar.exe"

    def __init__(self):
        self.info = " "
        self.url = "https://www.qq.com"
        self.introduce = f"""
        -------------   SaossionPage浏览器----------------------
        使用的浏览器:{self.browser_path}
        
        """

    def showinfo(self):
        # print(self.logo)
        print(self.introduce)


# -------------浏览器类 ----------
class Browser:
    def __init__(self, browser_path):
        self.browser_path = browser_path
        self.co = ChromiumOptions()
        self.co.set_browser_path(self.browser_path)
        self.co.set_argument("--hide-crash-restore-bubble")

        self.page = ChromiumPage(addr_or_opts=self.co)

        self.tabs = []
        self.eles = {}
        self.cmd = r"""
                    function loadjQuery() {
                      // 创建一个 script 元素
                      var script = document.createElement('script');
                    
                      // 设置 script 元素的 src 属性为 jQuery 的 CDN 地址
                      script.src = 'https://code.jquery.com/jquery-3.6.0.min.js';
                      script.id = 'jq';
                    
                      // 将 script 元素添加到文档的头部或 body 中
                      document.head.appendChild(script);
                      // 或者使用 document.body.appendChild(script);
                    }
                    loadjQuery();
                    """
        self.jiekou = [
            "https://www.ckplayer.vip/jiexi/?url=",
            "https://jx.yparse.com/index.php?url=",
            "https://www.8090g.cn/?url=",
            "https://www.ckplayer.vip/jiexi/?url=",
            "https://jx.qqwtt.com/?url=",
            "https://www.pouyun.com/?url=",
            "https://jx.m3u8.tv/jiexi/?url=",
            "https://z1.m1907.top/?jx=",
            "https://www.8090.la/8090/?url=",
            "https://www.pangujiexi.com/jiexi/?url=",
            "https://dmjx.m3u8.tv/?url=",
            "https://vip.bljiex.com/?v=",
            "https://www.mtosz.com/m3u8.php?url=",
            "https://www.playm3u8.cn/jiexi.php?url=",
            "https://www.yemu.xyz/?url=",
            "https://jx.m3u8.tv/jiexi/?url=",
            "https://api.qianqi.net/vip/?url=",
            "https://jx.playerjy.com/?url=",
            "https://jx.we-vip.com/?url=",
            "https://www.8090g.cn/jiexi/?url=",
            "https://vip.mpos.ren/v/?url=",
            "https://movie.heheda.top/?v=",
            "http://vip.wandhi.com/?v=",
            "https://jx.jsonplayer.com/player/?url=",
            "https://jx.playerjy.com/?url=",
            "https://jx.xmflv.com/?url=",
            "https://jx.xmflv.cc/?url=",
            "https://jx.yparse.com/index.php?url=",
            "https://im1907.top/?jx=",
            "https://www.8090g.cn/?url=",
            "https://api.qianqi.net/vip/?url=",
            "https://jx.yangtu.top/?url=",
            "https://www.ckplayer.vip/jiexi/?url=",
        ]

    # def start(self, url):
    #     # 创建页面对象，并启动或接管浏览器
    #     self.page = ChromiumPage(addr_or_opts=self.co)
    #     self.page.get(url)

    def open(self, url):
        self.tabs.append(self.page.new_tab(url))
        return self

    @property
    def newest_page(self):
        return self.page.get_tab(self.page.latest_tab)

    def download_path(self, path):
        self.page.set.download_path(path)
        return self

    def download(self, url):
        self.page.download(url)
        return self

    def show_title(self):
        print(self.tab.title)
        return self

    def max(self):
        self.page.set.window.max()
        return self

    def min(self):
        self.page.set.window.mini()
        return self

    def hide(self):
        self.page.set.window.hide()
        return self

    def show(self):
        self.page.set.window.show()
        return self

    def wait(self, num: int):
        self.page.actions.wait(num)
        return self

    def vip_open(self, url):
        self.page.get(self.jiekou[0] + url)

    def help(self, keyword):
        h = Help()
        h.doc(keyword=keyword)
        return self

    @property
    def gpt(self):
        return GPT(self.page)

    @property
    def jquery(self):
        return Jquery(self)

    def elements(self, k: str, v: str):
        ele = self.tab.eles(f"@{k}={v}")
        return ele

    @staticmethod
    def read_file(file_name):
        with open(file_name, "r", encoding="utf-8") as file:
            content = file.read()
        return content

    def run(self, script_file: str):
        _page = self.newest_page
        _page.run_js(Browser.read_file(script_file))

    def loadjQuery(self):
        if self.newest_page.ele("#jq", timeout=0.2):
            print("jQuery 已经加载")
        else:
            self.newest_page.run_js(self.cmd)
            print("jQuery 成功加载入页面...")

    @property
    def tab(self):  # 返回最新的标签页
        return self.page.get_tab(self.page.latest_tab)

    def download_all_img(self, tag):
        """
        从给定的标签中下载所有图片。

        参数:
        self: 当前对象
        tag: 包含要下载图片的标签对象

        返回值:
        self: 返回当前对象
        """
        for i in tag.eles("t:img"):
            for j in ["png", "jpg", "jpeg", "webp", "gif", "tiff"]:
                if j in i.link:
                    self.page.download(i.link)

        return self


# ----------------jQuery 类----------------
class Jquery:
    def __init__(self, browser: Browser):
        self.b = browser
        self.cmd = r"""
                    function loadjQuery() {
                  // 创建一个 script 元素
                  var script = document.createElement('script');
                
                  // 设置 script 元素的 src 属性为 jQuery 的 CDN 地址
                  script.src = 'https://code.jquery.com/jquery-3.6.0.min.js';
                  script.id = 'jq';
                
                  // 将 script 元素添加到文档的头部或 body 中
                  document.head.appendChild(script);
                  // 或者使用 document.body.appendChild(script);
                }
                loadjQuery();
                """
        self.load_jquery()

    def load_jquery(self):
        if self.b.newest_page.ele("#jq"):
            print("jQuery 已经加载")
        else:
            self.run(self.cmd)
            print("jQuery 成功加载入页面...")

    def run(self, js_str: str):
        self.b.newest_page.run_js(js_str)
        return self

    def exe(self, js_str: str):  # 有返回值
        return self.b.newest_page.run_js(js_str)


# ---------帮助类--------------
class Help:
    def __init__(self) -> None:
        self.info = [
            ["写法", "精确匹配", "模糊匹配", "匹配开头", "匹配结尾", "说明"],
            ["@属性名 ", "@属性名=", "@属性名:", "@属性名^", "@属性名$", "按某个属性查找"],
            ["@!属性名 ", r"@!属性名=", "@!属性名:", "@!属性名^", "@!属性名$", "查找属性不符合指定条件的元素"],
            ["text", "text=", "text:或不写", "text^", "text$", "按某个文本查找"],
            [
                "@text()",
                "@text()=",
                "@text():",
                "text()^",
                "text()$",
                "text与@或@@配合使用时改为text()，常用于多条件匹配",
            ],
            ["tag", "tag=或tag:", "无", "无", "无", "查找某个类型的元素"],
            ["xpath", "xpath=或xpath:", "无", "无", "无", "用 xpath 方式查找元素"],
            ["css", "css=或css:", "无", "无", "无", "用 css selector 方式查找元素"],
        ]
        self.chrome_command_line_arguments = [
            ["参数", "参数说明"],
            ["--disable-extensions", "禁用扩展"],
            ["--disable-popup-blocking", "禁用弹出窗口阻止功能"],
            ["--incognito", "以隐身模式启动"],
            ["--disable-plugins", "禁用插件"],
            ["--disable-translate", "禁用翻译功能"],
            ["--disable-notifications", "禁用通知"],
            ["--headless", "以无头模式（无界面）启动"],
            ["--disable-gpu", "禁用 GPU 硬件加速"],
            ["--remote-debugging-port=<port>", "指定远程调试端口"],
            ["--user-data-dir=<directory>", "指定用户数据目录"],
            ["--disable-web-security", "禁用跨域安全策略"],
            ["--proxy-server=<proxy>", "指定代理服务器"],
            ["--allow-file-access-from-files", "允许文件访问本地文件"],
            ["--disable-webgl", "禁用 WebGL"],
            ["--disable-sync", "禁用同步功能"],
            ["--disable-remote-fonts", "禁用远程字体加载"],
            # 添加更多参数...
        ]

    def doc(self, keyword: str):
        if "定位语法" in keyword:
            print('----------语法定位帮助-----------')
            print(
                tabulate(self.info[1:], headers=self.info[0], tablefmt="simple_outline")
            )
        if "启动参数" in keyword:
            print('----------启动参数帮助-----------')
            print(
                tabulate(self.chrome_command_line_arguments[1:], headers=self.chrome_command_line_arguments[0],
                         tablefmt="simple_outline")
            )


# -------------------GPT类----------------------------

class GPT:
    def __init__(self, page: ChromiumPage) -> None:
        self.url = 'https://chat-shared3.zhile.io/'
        self.page = page

    def auto_login(self):

        self.page.get(self.url)
        if self.page.ele('New Chat', timeout=1):
            print('已经登陆过...')
        else:
            if self.page.ele('OK'):
                self.page.ele('OK').click()
                self.page.wait(2)
                print('正在登入gpt,请等待...')
            ele = self.page.ele('t:ul@@class=flex-list').eles('t:li')

            e = Tool.get_random_element(ele)
            print(e.text)
            e.click()

            self.page.ele('不少于8位，须包含数字、字母').input('Admin@123')
            self.page.ele('OK').click()


# ------------工具类----------
class Tool:

    @staticmethod
    def get_random_element(input_list) -> ChromiumElement:
        """
        从输入列表中随机选择一个元素并返回。

        :param input_list: 输入的列表
        :return: 随机选择的元素
        """
        if not input_list:
            return None  # 返回 None，如果列表为空

        return random.choice(input_list)

    @staticmethod
    def sniff_and_download_video(
            page, kw: str = 'x://*[@id="post"]/article/div[3]/div'
    ):
        player = page.ele(kw)
        page.actions.wait(2).click(player)
        player.drag(50, 50, 2)
        player.click.at(40, 70)
        print("视频下载中.......")

    @staticmethod
    def sniff_and_download_videos(ele: ChromiumElement):
        # 执行嗅探并下载视频
        player = ele  # 定义变量player，表示ChromiumElement对象

        time.sleep(2)  # 等待2秒
        player.drag(50, 50, 2)  # 拖动player对象到坐标(50, 50)并移动2像素
        player.click.at(40, 70)  # 在坐标(40, 70)处单击player对象
        print("视频下载中.......")  # 打印提示信息"视频下载中......."

    @staticmethod
    def download_img(page):
        for picture in page("@itemprop=articleBody").eles("t:img"):
            picture.save(path=page.title)
            print("saving the picture..." + str(picture.tag))

    @staticmethod
    def click_next(page):
        page.ele("text:下一篇").click()
        time.sleep(3)

    @staticmethod
    def screenshot(ele, name="viewer"):
        ele.get_screenshot(name=name, scroll_to_center=True)

    @staticmethod
    def tree(ele):
        init()
        e = ele
        print(f"{Fore.BLUE}{Fore.CYAN}<{e.tag}>  {Fore.RESET}{e.attrs}")
        Tool.__tree(e)

    @staticmethod
    def __tree(ele: any, layer=7, has_next_brother=True, body=""):
        if ele.tag == "iframe":
            # ele = page.get_frame(ele)
            ele = ele("x:/html")
            # print(ele.html)
            # print(ele.children())
        try:
            list_ele = ele.children(timeout=0.1)
        except:
            list_ele = []
            print(ele)
            print("无法获取该元素子元素")

        length = len(list_ele)
        body_unit = "│   " if has_next_brother else "    "
        tail = "├───"
        new_body = body + body_unit

        if length > 0 and layer >= 1:
            has_next_brother2 = True
            for i in range(length):
                if i == length - 1:
                    tail = "└───"
                    has_next_brother2 = False
                e = list_ele[i]
                all_body = f"{Fore.BLUE}{new_body}{tail}{Fore.RESET}"

                print(f"{all_body}{Fore.CYAN}<{e.tag}>{Fore.RESET} ")
                Tool.tree_attr(e, all_body, has_next_brother2, layer)

                Tool.__tree(e, layer - 1, has_next_brother2, new_body)

    @staticmethod
    def tree_attr(ele, body, has_next_brother=True, layer=3):
        e: dict = ele.attrs
        has_child = True if ele.tag == "iframe" or ele.child(timeout=0.2) else False

        if layer == 1:
            has_child = False

        part1 = "│" if has_next_brother else " "
        part2 = "│" if has_child else " "
        replace_part = part1 + "   " + part2
        new_body = body.replace("├───", replace_part).replace("└───", replace_part)

        text = "" if ele.tag == "iframe" else ele.text.split("\n")[0]
        if len(text) >= 1:
            e["inner_txt"] = text if len(text) < 150 else text[0:150] + "......"

        if len(e) > 0:
            e["xpath"] = ele.xpath

            max_k_len = max([len(key) for key in e.keys()])
            head = "┌" + "─" * max_k_len + "┐"
            tail = "└" + "─" * max_k_len + "┘"
            print(new_body, head)

            for k, v in e.items():
                key = Fore.GREEN + str(k).ljust(max_k_len) + Fore.RESET + "│"
                content = f"{key}: {v}"

                print(new_body, "│" + key, v)

            print(new_body, tail)


# ---------------------AutoFill 类-----------------------------

class AutoFill:
    def __init__(self):
        pass

    @staticmethod
    def open_xl_list(file_name, sort_key=None):
        """
        打开excel, 表头只占一行, 数据从第二行开始, 返回排序好的字典列表

        :param file_name: Excel文件名
        :param sort_key: 排序关键字，默认为表头的第一列
        :return: 排序好的字典列表
        """
        if '.xls' not in file_name:
            file_name += '.xlsx'
        sheet = openpyxl.load_workbook(file_name).active
        data_list = []
        titles = []

        # 获取表头
        for cell in list(sheet.rows)[0]:
            titles.append(str(cell.value))

        # 读取数据并生成字典列表
        for row in list(sheet.rows)[1:]:
            data_obj = {}
            for i in range(len(titles)):
                data_obj[titles[i]] = row[i].value
            data_list.append(data_obj)

        # 根据排序关键字对列表进行排序
        return sorted(data_list, key=lambda x: x[sort_key or titles[0]])

    @staticmethod
    def form_value(form_ele, data_dict):
        """
        传入 form 元素和内容字典，将 form 中相匹配的 name 的 value 填入

        :param form_ele: form 元素
        :param data_dict: 内容字典
        """
        for ele in form_ele.eles('t:input'):
            if ele.attr('name') in data_dict:
                ele.set.attr('value', data_dict[ele.attr('name')])


# ---------------- 下面的是测试代码-------------------
if __name__ == "__main__1":
    # 连接浏览器
    browser = Browser(Config.browser_path)

    # 黑魔法一 观看vip视频
    browser.vip_open("https://v.qq.com/x/cover/mzc00200whsp9r6/j0047aj1c1n.html?ptag=11972")

if __name__ == "__main__2":
    # 连接浏览器
    browser = Browser(Config.browser_path)
    # 黑魔法二  查看某个元素的子元素结构树
    browser.open("https://www.qq.com/")
    body = browser.newest_page("x:/html/body")
    Tool.tree(body)

if __name__ == "__main__3":
    # 连接浏览器
    browser = Browser(Config.browser_path)
    # 黑魔法三  调用jQuery操作网页
    browser.loadjQuery()
    browser.run(r'$("div").css("color", "red");')

if __name__ == "__main__":
    # 连接浏览器
    browser = Browser(Config.browser_path)

    # 黑魔法四 实时查看库的帮助文档
    browser.help('定位语法')
    browser.help('启动参数')

if __name__ == "__main__5":
    # 连接浏览器
    browser = Browser(Config.browser_path)

    # 自动登入GPT
    browser.gpt.auto_login()

    browser.wait(55)

if __name__ == "__main__6":
    # 连接浏览器
    browser = Browser(Config.browser_path2)

    # 嗅探视频并下载  需要配合心愿浏览器
    browser.open('https://movie.douban.com/trailer/314095/#content')

    # 定位页面中的视频标签
    video_player = browser.newest_page('t:video')

    # 从视频标签中下载视频
    Tool.sniff_and_download_videos(video_player)

    browser.wait(55)
