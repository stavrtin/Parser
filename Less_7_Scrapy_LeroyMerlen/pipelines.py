# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient

class LeruaMerlenPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)       # формируем БД
        self.mongo_lm = client.LeroyMerlen              # создаем коллекцию в БД


    def process_item(self, item, spider):

        item['_id'] = item['link']               # обеспечим уникальность записей при вводе в Монго
        # del item['photo']                        # фото не закидываем в МОНГО
        collection = self.mongo_lm[spider.name]  # вносим в БД
        collection.insert_one(item)              # вносим в БД

        return item

class LeroyPhotoPipline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photo']:
            for img in item['photo']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        item['photo'] = [itm[1] for itm in results if itm[0]]
        return item

    # def file_path(self, request, response=None, info=None, *, item=None):
    #     # свой алгоритм формирования наименования скачанных файлов
    #     return ''  # своя реализация, которая будет возвращать нам путь к фото