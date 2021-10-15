from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from jobparser_my import settings
from jobparser_my.spiders.hhru import HhruSpider
from jobparser_my.spiders.sjfinder import SjfinderSpider

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings) # подтягивает наши настройки

    # для организации поиска (внесение запроса в поисковую строку)
    query = 'Data analytics'

    process = CrawlerProcess(settings=crawler_settings) # процессу передали наши настройки  создали авто
    process.crawl(HhruSpider, query=query)                           # посадили водителя - нашего паука
    process.crawl(SjfinderSpider, query=query)

    process.start()              # в момент вызова СТАРТ сможем попадать внутрь метода PARSE (hh.py)

