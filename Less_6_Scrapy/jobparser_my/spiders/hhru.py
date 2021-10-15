# https://hh.ru/search/vacancy?fromSearchLine=true&text=python&area=1&search_field=description&search_field=company_name&search_field=name
# https://hh.ru/search/vacancy?fromSearchLine=true&text=python&area=2&search_field=description&search_field=company_name&search_field=name
import scrapy
from scrapy.http import HtmlResponse
from jobparser_my.items import JobparserMyItem

class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    # start_urls =  ['https://hh.ru/search/vacancy?fromSearchLine=true&text=python&area=1&search_field=description&search_field=company_name&search_field=name',
    #               'https://hh.ru/search/vacancy?fromSearchLine=true&text=python&area=2&search_field=description&search_field=company_name&search_field=name']

    def __init__(self, query):
        # для организации поиска (внесение запроса в поисковую строку)
        super().__init__()       # ызываем родительсктй конструктор (что б ыне сломать родительские методы)
        self.start_urls = [f'https://hh.ru/search/vacancy?fromSearchLine=true&text={query}&area=1&search_field=description&search_field=company_name&search_field=name',
                           f'https://hh.ru/search/vacancy?fromSearchLine=true&text={query}&area=2&search_field=description&search_field=company_name&search_field=name']

    def parse(self, response:HtmlResponse):
        # перебирает вакансии по ссылкам и запускает линки в ваканси_парс
        next_page = response.xpath("//a[@data-qa='pager-next']/@href").get() #
        if next_page:                                                        # переход на след страницу сайта
            yield response.follow(next_page, callback=self.parse)            #
        links = response.xpath("//a[@data-qa='vacancy-serp__vacancy-title']/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)


    def vacancy_parse(self, response:HtmlResponse):
        # логика для обработки страницы
        name = response.xpath('//h1[@data-qa="vacancy-title"]/text()').get()
        salary = response.xpath('//p[@class="vacancy-salary"]/span[@data-qa="bloko-header-2"]/text()').getall()
        link = response.url
        company = response.xpath('//a[@class="vacancy-company-name"]//text()').getall()
        city = response.xpath('//p[@data-qa="vacancy-view-location"]/text()').getall()
        item = JobparserMyItem(name=name, salary=salary, link=link, city=city, company=company)
        yield item
        print()
