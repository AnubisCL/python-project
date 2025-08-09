# from scrapy.cmdline import execute
# import sys
# import os
#
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))
#
# execute(['scrapy', 'crawl', 'myblog'])  # 你需要将此处的spider_name替换为你自己的爬虫名称
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

if __name__ == '__main__':
    process = CrawlerProcess(get_project_settings())
    process.crawl('myblog')    #  你需要将此处的spider_name替换为你自己的爬虫名称
    process.start()
