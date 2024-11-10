'''
1) Создать пауков по сбору данных о книгах с сайтов labirint.ru и/или book24.ru
2) Каждый паук должен собирать:
* Ссылку на книгу
* Наименование книги
* Автор(ы)
* Основную цену
* Цену со скидкой
* Рейтинг книги
3) Собранная информация должна складываться в базу данных'''

import scrapy
from scrapy.http import HtmlResponse
from parse_lab.items import ParseLabItem

class LabSpiderSpider(scrapy.Spider):
    name = 'lab_spider'
    allowed_domains = ['labirint.ru']
    start_urls = ['https://www.labirint.ru/search/%D0%BA%D0%BE%D1%81%D0%BC%D0%BE%D1%81/?stype=0']

    def __init__(self, query):
        super().__init__()
        self.start_urls = [f'https://www.labirint.ru/search/{query}/?stype=0']

    def parse(self, response:HtmlResponse):
        # перебирает вакансии по ссылкам и запускает линки в ваканси_парс
        # next_page = response.xpath("//a[@class='pagination-next__text']/@href").get() #
        # if next_page:                                                        # переход на след страницу сайта
        #     yield response.follow(next_page, callback=self.parse)            #

        links = response.xpath('//a[@class="cover"]/@href').getall()
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)

    def vacancy_parse(self, response:HtmlResponse):
        # логика для обработки страницы
        name = response.xpath('//div[@id="product-title"]/h1/text()').get()
        author = response.xpath('//div[@class="authors"]//text()').getall()
        cost_old = response.xpath('//span[@class="buying-priceold-val-number"]/text()').get()
        cost = response.xpath('//span[@class="buying-price-val-number"]/text()').get()
        sale = response.xpath('//span[@class="buying-pricenew-val-number"]/text()').get()

        link = response.url
        rate = response.xpath('//div[@id="rate"]/text()').get()
        item = ParseLabItem(name=name, author=author, cost=cost, link=link,  sale=sale, rate=rate, cost_old=cost_old)
        yield item
        print()
