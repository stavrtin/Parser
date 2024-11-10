# импортируем библиотеки

from bs4 import BeautifulSoup as bs
from pprint import pprint
import re
import pandas as pd
# для MongoDB
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError as dke


# Библиотека для работы с HTTP-запросами. Будем использовать ее для обращения к API HH
import requests
# Пакет для удобной работы с данными в формате json
import json
# Модуль для работы со значением времени
import time


client = MongoClient('127.0.0.1', 27017)
db = client['parse_hh_1']
parse_hh_1 = db.parse_hh_1


def get_page(page=0, id=''):
    # Справочник для параметров GET-запроса
    params = {
        'id': id,
        'text': '',  # Текст фильтра. В имени должно быть слово "Аналитик"
        'area': 1,  # Поиск ощуществляется по вакансиям города Москва
        'page': page,  # Индекс страницы поиска на HH
        'specialization' : 1,
         'per_page': 100  # Кол-во вакансий на 1 странице
    }

    req = requests.get('https://api.hh.ru/vacancies', params)  # Посылаем запрос к API
    data = req.content.decode()  # Декодируем его ответ, чтобы Кириллица отображалась корректно
    req.close()
    return data


# Создаем список, в котором будут хранится ответы запроса к сервису API hh.ru
vacant_id = []

# Считываем первые 2000 вакансий
for page in range(0, 2):

    # Преобразуем текст ответа запроса в словарь Python
    js_obj = json.loads(get_page(page))

    for item in range(len(js_obj.get('items'))):
        vacant_id.append(js_obj.get('items')[item].get('id'))

    # Проверка на последнюю страницу, если вакансий меньше 2000
    if (js_obj['pages'] - page) <= 1:
        break
    # Необязательная задержка, но чтобы не нагружать сервисы hh, оставим. 5 сек мы может подождать
    time.sleep(0.25)

print(len(vacant_id))


def get_info(id):
    # Справочник для параметров GET-запроса
    # params = {'id': id}
    url = 'https://api.hh.ru/vacancies/' + id
    req = requests.get(url)  # Посылаем запрос к API
    data = req.content.decode()  # Декодируем его ответ, чтобы Кириллица отображалась корректно
    req.close()
    # vacant_info = get_vacant_info(data)
    js_obj = json.loads(data)
    vacant_info_dict = {}
    try:
        vacant_info_dict['name'] = js_obj.get('name')
    except:
        vacant_info_dict['name'] = None
    try:
        vacant_info_dict['area'] = js_obj.get('area').get('name')
    except:
        vacant_info_dict['area'] = None
    try:
        vacant_info_dict['salary_min'] = js_obj.get('salary').get('from')
    except:
        vacant_info_dict['salary_min'] = None

    try:
        vacant_info_dict['salary_max'] = js_obj.get('salary').get('to')
    except:
        vacant_info_dict['salary_max'] = None

    try:
        vacant_info_dict['salary_currency'] = js_obj.get('salary').get('currency')
    except:
        vacant_info_dict['salary_currency'] = None

    try:
        vacant_info_dict['experience'] = js_obj.get('experience').get('name')
    except:
        vacant_info_dict['experience'] = None

    try:
        vacant_info_dict['schedule'] = js_obj.get('schedule').get('name')
    except:
        vacant_info_dict['schedule'] = None

    try:
        vacant_info_dict['description'] = js_obj.get('description')
    except:
        vacant_info_dict['description'] = None

    try:
        vacant_info_dict['employment'] = js_obj.get('employment').get('name')
    except:
        vacant_info_dict['employment'] = None

    try:
        vacant_info_dict['key_skills'] = js_obj.get('key_skills')
    except:
        vacant_info_dict['key_skills'] = None

    try:
        vacant_info_dict['employer'] = js_obj.get('employer').get('id')
    except:
        vacant_info_dict['employer'] = None

    try:
        vacant_info_dict['professional_roles'] = js_obj.get('professional_roles')#.get('name')
    except:
        vacant_info_dict['professional_roles']  = None

    try:
        vacant_info_dict['specializations'] = js_obj.get('specializations')#.get('profarea_name')
    except:
        vacant_info_dict['specializations'] = None



    try:
        parse_hh_1.insert_one({'_id': int(id),
                              'name': vacant_info_dict['name'],
                              'area': vacant_info_dict['area'],
                              'salary_min': vacant_info_dict['salary_min'],
                             'salary_max': vacant_info_dict['salary_min'],
                            'salary_currency': vacant_info_dict['salary_currency'],
                            'experience': vacant_info_dict['experience'],
                            'schedule': vacant_info_dict['schedule'],
                            'description': vacant_info_dict['description'],
                            'employment': vacant_info_dict['employment'],
                            'employer': vacant_info_dict['employer'],
                            'professional_roles': vacant_info_dict['professional_roles'],
                            'specializations': vacant_info_dict['specializations']
                              })


    except: dke

    return vacant_info_dict

vacant_dict = []
count = 0
for item_id in vacant_id:
    vacant_dict.append(get_info(item_id))
    if count % 100 == 0:
        time.sleep(0.2)
    count += 1

print(len(vacant_dict))



print(vacant_id[1])





#
#
# def parser_hh(vacancy_name):
#     url = 'https://hh.ru'
#     full_url = url + '/search/vacancy'
#     vacancy = vacancy_name
#
#      #####################################
#     client = MongoClient('127.0.0.1', 27017)
#     db = client['vacant']
#     vacant_db = db.vacant_db
#
#
#     #     зададим параметры поиска и заголовки
#     params = {'text': vacancy
#               }
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 YaBrowser/21.8.3.614 Yowser/2.5 Safari/537.36'}
#
#     vacancy_data = []
#
#     while True:
#         response = requests.get(full_url, headers=headers, params=params)
#
#         #       получим ДОМ
#         soup = bs(response.text, 'html.parser')
#
#         #       найдем блоки, содержащие сведения по вакансии
#         vacancy_list = soup.find_all('div', attrs={'class': 'vacancy-serp-item'})
#
#         #     из массива блоков вакансий возьмем каждый и выделим интересующие нас поля
#         for vacant in vacancy_list:
#             vacant_dict = {}
#             salary_min = 'Nan'
#             salary_max = 'Nan'
#             #           наименование вакансии
#             vacant_name = vacant.find('div', attrs={'class': 'vacancy-serp-item__info'}).text
#             #           ссылка на вакансию
#             vacant_link = vacant.find('a', attrs={'class': 'bloko-link'})['href']
#             #           город вакансии
#             vacant_town = vacant.find('span', attrs={'class': 'vacancy-serp-item__meta-info'}).text
#             #           организация
#             vacant_plant = vacant.find('div', {'class': 'vacancy-serp-item__meta-info'}).find('a').getText()
#             # чистим поле организации от мусора
#             if vacant_plant.find('\xa0') != -1:
#                 vacant_plant = vacant_plant.replace('\xa0', ' ')
#
#             vacant_dict['Name'] = vacant_name
#             vacant_dict['Link'] = vacant_link
#             vacant_dict['Town'] = vacant_town
#             vacant_dict['Company'] = vacant_plant
#
#             #           зарплата по вакансии: почистим и разнесем по полям "мин" "макс" и "валюта"
#             try:
#                 vacant_salary = vacant.find('div', attrs={'class': 'vacancy-serp-item__sidebar'}).text
#                 if vacant_salary.find('\u202f') != -1:
#                     vacant_salary = vacant_salary.replace('\u202f', ' ')
#                 if vacant_salary == ' ' or vacant_salary == '':
#                     vacant_salary = 'Nan'
#
#             except:
#                 vacant_salary = 'Nan'
#
#             if vacant_salary != 'Nan':
#                 vacant_salary = re.split(r'\s|-', vacant_salary)
#                 if vacant_salary[0] == 'до':
#                     salary_min = None
#                     salary_max = int(vacant_salary[1]) * 1000
#                 elif vacant_salary[0] == 'от':
#                     salary_min = int(vacant_salary[1]) * 1000
#                     salary_max = None
#                 else:
#                     salary_min = int(vacant_salary[0]) * 1000
#                     salary_max = int(vacant_salary[3]) * 1000
#
#                 salary_currency = vacant_salary[len(vacant_salary) - 1]
#
#                 vacant_dict['Salary_min'] = salary_min
#                 vacant_dict['Salary_max'] = salary_max
#                 vacant_dict['Currency'] = salary_currency
#
#             else:
#                 vacant_dict['Salary_min'] = 'Nan'
#                 vacant_dict['Salary_max'] = 'Nan'
#                 vacant_dict['Currency'] = 'Nan'
#
#             if (vacant_dict['Salary_min'] !=  'Nan') and (vacant_dict['Salary_max'] !=  'Nan'):
#                 salary_currency = vacant_salary[len(vacant_salary) - 1]
#             else: salary_currency = 'Nan'
#
#             vacant_dict['Site'] = 'hh.ru'
#
#             try:
#                 vacant_db.insert_one({'_id': vacant_link,
#                                     'Name': vacant_name,
#                                     'Link': vacant_link,
#                                     'Town': vacant_town,
#                                     'Salary_min': salary_min,
#                                     'Salary_max': salary_max,
#                                     'Company': vacant_plant,
#                                     'Currency': salary_currency,
#                                     'Site': "hh.ru"
#                                     })
#             except dke:
#                 continue
#
#             vacancy_data.append(vacant_dict)
#
#
#         # организовываем переход на следующую страницу
#         next = soup.find('a', attrs={'data-qa': 'pager-next'})
#         if next:
#             full_url = url + next['href']
#         else:
#             break
#
#     return vacancy_data
#
#
# def parser_sj(vacancy_name):
#
#     client = MongoClient('127.0.0.1', 27017)
#     db = client['vacant']
#     vacant_db = db.vacant_db
#
#
#     url = 'https://www.superjob.ru'
#     full_url = url + '/vacancy/search/'
#     vacancy = vacancy_name
#     page = 1
#     params = {'keywords': vacancy,
#               'noGeo': 1,
#               'page': page
#               }
#
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 YaBrowser/21.8.3.614 Yowser/2.5 Safari/537.36'}
#
#     vacancy_data = []
#
#     while True:
#
#         response = requests.get(full_url, headers=headers, params=params)
#         soup = bs(response.text, 'html.parser')
#         vacancy_list = soup.find_all('div', attrs={'class': 'f-test-vacancy-item'})
#
#         if not vacancy_list or not response.ok:
#             break
#
#         for vacant in vacancy_list:
#             vacant_dict = {}
#             salary_min = 'Nan'
#             salary_max = 'Nan'
#             vacant_block = vacant.find('div', attrs={'class': '_1h3Zg _2rfUm _2hCDz _21a7u'})
#             vacant_name = vacant_block.text
#             vacant_link = url + vacant_block.find('a', attrs={'class': 'icMQ_'})['href']
#             vacant_town = vacant.find('span', {'class': 'f-test-text-company-item-location'}).findChildren()[2].text
#
#
#             try:
#                 vacant_plant = vacant.find('span', attrs={'class': 'f-test-text-vacancy-item-company-name'}).text
#             except:
#                 vacant_plant = 'Nan'
#
#
#             vacant_dict['Town'] = vacant_town
#             vacant_dict['Company'] = vacant_plant
#
#             try:
#                 vacant_salary = vacant.find('span', attrs={'class': '_1h3Zg'}).text
#                 if vacant_salary.find('\xa0') != -1:
#                     vacant_salary = vacant_salary.replace('\xa0', ' ')
#                     vacant_salary = re.split(r'\s|-', vacant_salary)
#
#                     if vacant_salary[0] == 'до':
#                         salary_min = 'Nan'
#                         salary_max = int(vacant_salary[1]) * 1000
#                     elif vacant_salary[0] == 'от':
#                         salary_min = int(vacant_salary[1]) * 1000
#                         salary_max = 'Nan'
#                     elif vacant_salary[0] == 'По':
#                         salary_min = 'Nan'
#                         salary_max = 'По договоренности'
#                     else:
#                         salary_min = int(vacant_salary[0]) * 1000
#                         salary_max = int(vacant_salary[3]) * 1000
#
#                 if vacant_salary == 'По договорённости':
#                     salary_currency = 'Nan'
#                 else:
#                     salary_currency = vacant_salary[len(vacant_salary) - 1]
#                 vacant_dict['Currency'] = salary_currency
#             except:
#                 vacant_salary = 'Nan'
#
#             vacant_dict['Name'] = vacant_name
#             vacant_dict['Link'] = vacant_link
#             vacant_dict['Site'] = "superjob.ru"
#
#             vacant_dict['Salary_min'] = salary_min
#             vacant_dict['Salary_max'] = salary_max
#             vacant_dict['Currency'] = salary_currency
#
#
#             try:
#                 vacant_db.insert_one({'_id': vacant_link,
#                                     'Name': vacant_name,
#                                     'Link': vacant_link,
#                                     'Town': vacant_town,
#                                     'Salary_min': salary_min,
#                                     'Salary_max': salary_max,
#                                     'Company': vacant_plant,
#                                     'Currency': salary_currency,
#                                     'Site': "hh.ru"
#                                     })
#             except dke:
#                 continue
#
#             vacancy_data.append(vacant_dict)
#         params['page'] += 1
#
#     return vacancy_data
#
#
# # функция объединения двух поисков в один датафрейм
# def parser_twin(vacancy):
#     df_hh = []
#     df_sj = []
#     df_hh = parser_hh(vacancy)
#     df_sj = parser_sj(vacancy)
#     df_hh.append(df_sj)
#
#     return print(len(df_hh) + len(df_sj))
#
#




