from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from parse_lab import settings
from parse_lab.spiders.lab_spider import LabSpiderSpider

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings) # подтягивает наши настройки

    # для организации поиска (внесение запроса в поисковую строку)
    query = 'фантастика'

    process = CrawlerProcess(settings=crawler_settings) # процессу передали наши настройки  создали авто
    process.crawl(LabSpiderSpider, query=query)                           # посадили водителя - нашего паука
    process.start()              # в момент вызова СТАРТ сможем попадать внутрь метода PARSE (hh.py)

