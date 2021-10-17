# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose,TakeFirst

def clear_price(value):
    try:                                                    #
       value = int(value.replace(' ', ''))                  # мелкую обработку производим
    except:                                                 # в items.py
        return value                                        #
    return value


class LeruaMerlenItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field(output_processor=TakeFirst())                          # 7й урок 2:20...2:35
    link = scrapy.Field(output_processor=TakeFirst())                          # 7й урок 2:31...2:35
    photo = scrapy.Field()                                                     # 7й урок 2:20...2:35
    price = scrapy.Field(input_processor=MapCompose(clear_price), output_processor=TakeFirst())
    title = scrapy.Field()
    _id = scrapy.Field()

