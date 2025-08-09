import scrapy

# 2.生成 模板命令 scrapy genspider myblog "127.0.0.1"
class ItcastSpider(scrapy.Spider):
    name = 'itcast'
    allowed_domains = ['itcast.cn']
    start_urls = ("http://www.itcast.cn/channel/teacher.shtml",)

    def parse(self, response):
        with open("teacher.html", "w", encoding="utf-8") as file:
            file.write(response.text)

# 3.运行 命令 scrapy crawl itcast （上name）
