# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import scrapy


class SpidertestItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

# 1.创建实体类
class MyspiderItem(scrapy.Item):
  url = scrapy.Field()
  title = scrapy.Field()
