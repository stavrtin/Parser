# Импортируем библиотеки
from pprint import  pprint
from lxml import html
import requests
# для MongoDB
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError as dke

headers = {'User Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 YaBrowser/21.9.0.1044 Yowser/2.5 Safari/537.36'}

all_news = []

def mail_news():
    url = 'https://news.mail.ru/'

    mail_news = []
    response = requests.get(url, headers=headers)
    dom = html.fromstring(response.text)

    url_photo = dom.xpath("//tr/td/div/a[contains(@class, 'photo_full ')]/@href")
    url_text = dom.xpath("//li[@class='list__item']/a[@class='list__text']/@href")

    url_photo.extend(url_text)

    for i in url_photo:

        response_inside = requests.get(i)
        dom_inside = html.fromstring(response_inside.text)

        news = {}
        names = dom_inside.xpath("//h1/text()")
        time_new = dom_inside.xpath("//span[@class='note__text breadcrumbs__text js-ago']/@datetime")
        links = i
        source = dom_inside.xpath("//span[@class='breadcrumbs__item']//a[@class='link color_gray breadcrumbs__link']//text()")

        news['name'] = names
        news['date'] = time_new
        news['link'] = links
        news['source'] = source
        mail_news.append(news)

    return mail_news




def lenta_main_news(all_news):
 # '''блок главных новостей'''
    url = 'https://lenta.ru/'

    response = requests.get(url, headers=headers)
    dom = html.fromstring(response.text)

    url_inside = dom.xpath("//div[@class='b-yellow-box__wrap']/div/a/@href")

    for i in url_inside[1:-1]:
        news = []
        response_inside = requests.get(url + i)
        dom_inside = html.fromstring(response_inside.text)

        news = {}
        names = dom_inside.xpath("//h1[@class='b-topic__title']/text()")
        time_new = dom_inside.xpath("//div[@class='b-topic__info']/time[@class='g-date']/@datetime")
        links = (url + i)

        news['name'] = names
        news['date'] = time_new
        news['link'] = links
        news['source'] = 'lenta.ru'

        all_news.append(news)
    return all_news

def lenta_second_news(all_news):
# """   блок доп. новостей"""
    url = 'https://lenta.ru/'

    response = requests.get(url, headers=headers)
    dom = html.fromstring(response.text)

    items = dom.xpath("//div[@class='span4']/div[@class='item']")

    for item in items:
        news = {}
        news_names = item.xpath("./a/text()")
        news_date = item.xpath(".//time[@class='g-time']/@datetime")
        news_link = url + item.xpath("./a/@href")[0]

        news['name'] = news_names
        news['date'] = news_date
        news['link'] = news_link
        news['source'] = 'lenta.ru'

        all_news.append(news)
    return all_news

def lenta_first_news(all_news):
# '''блок важнейшей новости '''
    url = 'https://lenta.ru/'

    response = requests.get(url, headers=headers)
    dom = html.fromstring(response.text)

    news = {}
    first_news = dom.xpath("//div[@class='first-item']//h2/a/text()")
    first_date = dom.xpath("//div[@class='first-item']//h2//time/@datetime")
    first_link = dom.xpath("//div[@class='first-item']//h2/a/@href")

    news['name'] = first_news
    news['date'] = first_date
    news['link'] = url + first_link[0]
    news['source'] = 'lenta.ru'
    all_news.append(news)

    return all_news

def lenta_send_to_db(all_news):
    # '''запись в БД MongoDB'''

    client = MongoClient('127.0.0.1', 27017)
    db = client['news']
    news_lenta = db.news_lenta

    for i in all_news:
        try:
            news_lenta.insert_one({'_id': i['link'],
                                   'Name': i['name'][0],
                                   'Link': i['link'],
                                   'Date': i['date'][0],
                                   'Source': i['source']
                                   })
        except:
            continue

    return all_news

def mail_send_to_db(mail_news):
    # '''запись mail новостей в БД MongoDB'''

    client = MongoClient('127.0.0.1', 27017)
    db = client['news']
    news_mail = db.news_mail

    for i in mail_news():
        try:
            news_mail.insert_one({'_id': i['link'],
                                   'Name': i['name'][0],
                                   'Link': i['link'],
                                   'Date': i['date'][0],
                                   'Source': i['source'][0]
                                   })
        except: continue

    return all_news


lenta_main_news(all_news)
lenta_second_news(all_news)
lenta_first_news(all_news)
lenta_send_to_db(all_news)
# pprint(mail_news())
mail_send_to_db(mail_news)

print('end')


