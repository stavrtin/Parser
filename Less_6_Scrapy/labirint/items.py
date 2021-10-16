# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ParseLabItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    author = scrapy.Field()
    cost = scrapy.Field()
    link = scrapy.Field()
    sale = scrapy.Field()
    rate = scrapy.Field()
    _id = scrapy.Field()
    cost_old = scrapy.Field()


