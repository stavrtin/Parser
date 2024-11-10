from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from gram_prj.spiders.gram import GramSpider
from gram_prj import settings


if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)

    process.crawl(GramSpider)
    process.start()