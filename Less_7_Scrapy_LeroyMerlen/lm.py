'''1) Взять любую категорию товаров на сайте Леруа Мерлен. Собрать следующие данные:
● название;
● все фото;
● ссылка;
● цена.
Реализуйте очистку и преобразование данных с помощью ItemLoader. Цены должны быть в виде числового значения.
Дополнительно:
2)Написать универсальный обработчик характеристик товаров, который будет формировать данные вне
зависимости от их типа и количества.
3)Реализовать хранение скачиваемых файлов в отдельных папках, каждая из которых должна
соответствовать собираемому товару'''

import scrapy
from scrapy.http import HtmlResponse
from lerua_merlen.items import LeruaMerlenItem
from scrapy.loader import ItemLoader           # для ускорения работы паука (из паука передаем в items)


class LmSpider(scrapy.Spider):
    name = 'lm'
    allowed_domains = ['leroymerlin.ru']
    # start_urls = ['https://leroymerlin.ru/search/?q=увлажнитель']

    def __init__(self, query):
        super().__init__()
        self.start_urls = [f'https://leroymerlin.ru/search/?q={query}']

    def parse(self, response: HtmlResponse):
        # перебирает вакансии по ссылкам и запускает линки в ваканси_парс
        # next_page = response.xpath("//a[@class='bex6mjh_plp s15wh9uj_plp l7pdtbg_plp r1yi03lb_plp sj1tk7s_plp']/@href").get() #
        # if next_page:                                                        # переход на след страницу сайта
        #     yield response.follow(next_page, callback=self.parse)            #

        links = response.xpath('//div[@class="phytpj4_plp largeCard"]/a/@href').getall()
        for link in links:
            yield response.follow(link, callback=self.parse_lerua)

    def parse_lerua(self, response: HtmlResponse):
        loader = ItemLoader(item=LeruaMerlenItem(), response=response)

        loader.add_value('link', response.url)
        loader.add_xpath('name', '//h1[@class="header-2"]/text()')
        loader.add_xpath('price','//span[@slot="price"]/text()')
        loader.add_xpath('photo', '//img[@itemprop="image"]/@data-origin')
        # loader.add_value('title', query)
        yield loader.load_item()

        # name = response.xpath('//h1[@class="header-2"]/text()').getall()
        # price = response.xpath('//span[@slot="price"]/text()').get()
        # photo = response.xpath('//img[@itemprop="image"]/@data-origin').getall()
        # link = response.url
        # item = LeruaMerlenItem(name=name, photo=photo, price=price, link=link)
        # yield item


