from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from lerua_merlen.spiders.lm import LmSpider
from lerua_merlen import settings


if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    query = 'увлажнитель'

    process.crawl(LmSpider, query=query)
    process.start()

