# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import hashlib
from scrapy.utils.python import to_bytes
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline


# useful for handling different item types with a single interface
import scrapy
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient

class GramPrjPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)       # формируем БД
        self.mongo_instagram = client.Instagram        # создаем коллекцию в БД


    def process_item(self, item, spider):
        print()
        collection_name = item['username']
        collection = self.mongo_instagram[collection_name]  # вносим в БД в нужную коллекцию
        collection.insert_one(item)              # вносим в БД

        return item


class InstagPhotoPipeLine(ImagesPipeline):
    def get_media_requests(self, item, info):
        print()
        if item['photo']:

            try:
                yield scrapy.Request(item['photo'])
            except Exception as e:
                print(e)

    def item_completed(self, results, item, info):
        item['photo'] = item['photo']
        return item

    def file_path(self, request, response=None, info=None, *, item=None):
        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()
        print()
        return f'full/{item["username"]}/{image_guid}.jpg'




