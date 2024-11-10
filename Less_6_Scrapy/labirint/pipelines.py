# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient

class ParseLabPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017) # формируем БД
        self.mongo_db = client.shop              # создаем коллекцию в БД

    def process_item(self, item, spider):
        item['author'] = self.process_author(item['author']) # обработка поля автор
        item['name'] = self.process_name(item['name'])       # обработка поля название
        item['cost'] = self.process_cost(item['cost'], item['cost_old'])       # обработка поля цена
        item['sale'] = self.process_sale(item['sale'])       # обработка поля скидка
        item['_id'] = item['link']  # обеспечим уникальность записей при вводе в Монго

        collection = self.mongo_db[spider.name]  # вносим в БД
        collection.insert_one(item)              # вносим в БД

        return item

    def process_author(self, author):
        if not author:
            author_name = None
        else:
            author_name = author[1]
        return author_name

    def process_name(self, name):
        if (': ' in name):
            name_str = name.split(': ')[1]
        else:
            name_str = name
        return name_str

    def process_cost(self, cost, cost_old):
        if not cost_old:
            cost_str = cost
        else:
            cost_str = None
        return cost_str

    def process_sale(self, sale):
        if not sale:
            sale_str = None
        else:
            sale_str = sale
        return sale_str