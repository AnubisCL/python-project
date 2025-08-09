from DrissionPage._configs.chromium_options import ChromiumOptions
from DrissionPage._functions.web import get_blob
from DrissionPage._pages.web_page import WebPage

if __name__ == '__main__':
    co = ChromiumOptions().set_browser_path(r"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
    page = WebPage(chromium_options=co)
    page.wait.load_start()