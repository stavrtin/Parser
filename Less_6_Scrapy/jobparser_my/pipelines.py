# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient

class JobparserMyPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_db = client.vacant

    def process_item(self, item, spider):

        if spider.name == 'hhru':
            item['salary_min'], item['salary_max'], item['currancy'] = self.process_salary(item['salary'])
            del item['salary']
            item['company'] = self.process_company(item['company'])
            item['city'] = self.process_city(item['city'])
            item['_id'] = item['link']
            collection = self.mongo_db[spider.name]
            collection.insert_one(item)

        else:
            item['salary_min'], item['salary_max'], item['currancy'] = self.process_salary_sj(item['salary'])
            del item['salary']
            item['company'] = self.process_company_sj(item['company'])
            item['city'] = self.process_city_sj(item['city'])
            item['_id'] = item['link']
            collection = self.mongo_db[spider.name]
            collection.insert_one(item)

        return item

    def process_salary(self, salary):
        if salary[0].find('з/п не указана') != -1:
            salary_min = 'Nan'
            salary_max = 'Nan'
            currancy = 'Nan'
        else:
            if salary[0].find('до') != -1:
                salary_min = None
                salary_max = int(salary[1].replace('\xa0',''))
            elif (salary[0].find('от') != -1) and ((salary[2].find('до') == -1)):
                salary_min = int(salary[1].replace('\xa0',''))
                salary_max = None
            else:
                salary_min = int(salary[1].replace('\xa0',''))
                salary_max = int(salary[3].replace('\xa0',''))
            currancy = salary[len(salary) - 2]

        return salary_min, salary_max, currancy

    def process_city(self, city):
        if (len(city) == 0):
            city_str = None
        elif len(city) == 1:
            city_str = city[0]
        elif len(city) > 1:
            city_str = ''.join(city)
        return city_str

    def process_company(self, company):
        if (len(company) == 0):
            company_str = None
        elif len(company) == 1:
            company_str = company[0]
        elif len(company) > 1:
            company_str = ''.join(company)
        return company_str

    def process_salary_sj(self, salary):
        if ('По договорённости' in salary):
            # ['По договорённости']
            salary_min = None
            salary_max = None
            currancy = None
        else:
            if salary[0].find('до') != -1:
                # ['до', '\xa0', '180\xa0000\xa0руб.']
                salary_min = None
                salary_max = int(salary[2].split('\xa0')[0])*1000
                currancy = salary[2].split('\xa0')[2]

            elif salary[2].find('до') != -1:
                # ['от ', '200\xa0000', ' до ', '300\xa0000', ' ', 'руб.', ' на руки']
                salary_min = int(salary[1].split('\xa0')[0]) * 1000
                salary_max = int(salary[3].split('\xa0')[0]) * 1000
                currancy = salary[5]

            elif ('от' in salary) and (len(salary) == 3):
                # ['от', '\xa0', '150\xa0000\xa0руб.']
                salary_min = int(salary[2].split('\xa0')[0])*1000
                salary_max = None
                currancy = salary[2].split('\xa0')[2]

            elif ('от' in salary) and ((' на руки' in salary) or (' до вычета налогов' in salary)):
                salary_min = int(salary[1].split('\xa0')[0])*1000
                salary_max = None
                currancy = salary[3]

            else:
                salary_min = int(salary[0].split('\xa0')[0])*1000
                salary_max = int(salary[1].split('\xa0')[0])*1000
                currancy = salary[3]

        return salary_min, salary_max, currancy

    def process_city_sj(self, city):
        if (len(city) == 0):
            city_str = None
        elif len(city) == 1:
            city_str = city[0]
        elif len(city) > 1 and city[0] != city[1]:
            city_str = ''.join(city)
        else: city_str = None

        return city_str

    def process_company_sj(self, company):
        if (len(company) == 0):
            company_str = None
        elif len(company) == 1:
            company_str = company[0]
        elif len(company) > 1:
            company_str = ''.join(company)
        return company_str
