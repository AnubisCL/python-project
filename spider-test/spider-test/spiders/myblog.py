import scrapy

from spiderTest.items import MyspiderItem

class MyblogSpider(scrapy.Spider):
    name = 'myblog'
    allowed_domains = ['127.0.0.1']
    start_urls = (
        'http://127.0.0.1',
    )

    def parse(self, response):
        # if response.text != '':
        #     text = response.text
        #     file = open('index.html', 'w', encoding='utf-8')  #
        #     file.write(text)
        #     file.close()
        #     print('file write finish!')
        items = [] #存放信息集合
        for each in response.xpath("//a[@class='btn']"):
           # 将我们得到的数据封装到一个'MyspiderItem'对象
           item = MyspiderItem()
           # extract方法返回的都是Unicode字符串
           url = each.attrib.get('href')
           title = each.root.text
           # XPath返回的是包含一个元素的列表
           item["url"] = url
           item["title"] = title
           items.append(item)
           # 返回数据，不经过pipeline
        if len(items) > 0:
            for item in items:
                url = item['url']
                title = item['title']
                file = open('index.html', 'a', encoding='utf-8')  #
                file.write('{ title:' + title + ', url:' + url + ' }\t\n')
                file.close()
                print('file write finish!')
        return items
#     xpath:
# scrapy crawl myblog