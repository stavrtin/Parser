# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GramPrjItem(scrapy.Item):
    # define the fields for your item here like:
    follower_user_id = scrapy.Field()
    follower_username = scrapy.Field()
    follower_full_name = scrapy.Field()
    photo = scrapy.Field()
    follower_user_data = scrapy.Field()

    followinger_user_id = scrapy.Field()
    followinger_username = scrapy.Field()
    followinger_full_name = scrapy.Field()
    followinger_user_data = scrapy.Field()
    username = scrapy.Field()




