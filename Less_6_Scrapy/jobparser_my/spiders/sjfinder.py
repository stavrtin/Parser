# https://www.superjob.ru/vacancy/search/?keywords=python&noGeo=1
import scrapy
from scrapy.http import HtmlResponse
from jobparser_my.items import JobparserMyItem

class SjfinderSpider(scrapy.Spider):
    name = 'sjfinder'
    allowed_domains = ['www.superjob.ru']
    # start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=python&noGeo=1']

    def __init__(self, query):
        super().__init__()  # ызываем родительсктй конструктор (что б ыне сломать родительские методы)
        self.start_urls = [f'https://www.superjob.ru/vacancy/search/?keywords={query}&noGeo=1']

    def parse(self, response:HtmlResponse):
        # перебирает вакансии по ссылкам и запускает линки в ваканси_парс
        next_page = response.xpath("//a[@class='icMQ_ bs_sM _3ze9n _2Pv5x f-test-button-dalshe f-test-link-Dalshe']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath("//div[@class='_2rfUm _2hCDz _21a7u']/a/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse_sj)


    def vacancy_parse_sj(self, response:HtmlResponse):
        # логика для обработки страницы
        name = response.xpath('//h1[@class="rFbjy _2dazi _2hCDz _1RQyC"]/text()').get()
        salary = response.xpath('//span[@class="_2Wp8I _2rfUm _2hCDz"]/text()').getall()
        link = response.url
        company = response.xpath('//h2[@class="_2rfUm _2hCDz _2ZsgW _21a7u _2SvHc"]//text()').getall()
        city = response.xpath('//span[@class="_1TK9I _2hCDz"]/text()').getall()[0]
        item = JobparserMyItem(name=name, salary=salary, link=link, city=city, company=company)
        yield item

        print()
