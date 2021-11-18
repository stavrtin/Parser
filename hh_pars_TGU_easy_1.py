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
db = client['parse_hh']
parse_hh_easy = db.parse_hh_easy


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



######################

def get_page(page=0):
    """
    Создаем метод для получения страницы со списком вакансий.
    Аргументы:
        page - Индекс страницы, начинается с 0. Значение по умолчанию 0, т.е. первая страница
    """
    vacant_info = []
    # Справочник для параметров GET-запроса
    params = {
        # 'id': id,
        'text': '',  # Текст фильтра. В имени должно быть слово "Аналитик"
        'area': 1,  # Поиск ощуществляется по вакансиям города Москва
        'page': page,  # Индекс страницы поиска на HH
        'specialization' : 1,
         'per_page': 100  # Кол-во вакансий на 1 странице
    }

    req = requests.get('https://api.hh.ru/vacancies', params)  # Посылаем запрос к API
    data = req.content.decode()  # Декодируем его ответ, чтобы Кириллица отображалась корректно
    req.close()

    vacant_info.append(get_vacant_info(data))

    return data

def get_long_info(id):
    url = 'https://api.hh.ru/vacancies/' + id
    req = requests.get(url)  # Посылаем запрос к API
    data_long = req.content.decode()  # Декодируем его ответ, чтобы Кириллица отображалась корректно
    req.close()
    return data_long



def get_vacant_info(data_js):
    js_obj = json.loads(data_js)
    vacant_info = {}
    for item in range(len(js_obj.get('items'))):
        # vacant_id_list = vacant_id_list.append(js_obj.get('items')[item].get('id'))

        # vacant_info['id'] = js_obj.get('items')[item].get('id')
        # vacant_info['name'] = js_obj.get('items')[item].get('name')
        # vacant_info['area'] = js_obj.get('items')[item].get('area').get('name')
        # vacant_info['salary_min'] = js_obj.get('items')[item].get('salary').get('from')
        # vacant_info['salary_max'] = js_obj.get('items')[item].get('salary').get('to')

        try:
            vacant_info['id'] = js_obj.get('items')[item].get('id')
        except:
            vacant_info['id'] = None

        try:
            vacant_info['name'] = js_obj.get('items')[item].get('name')
        except:
            vacant_info['name'] = None

        try:
            vacant_info['area'] = js_obj.get('items')[item].get('area').get('name')
        except:
            vacant_info['area'] = None

        try:
            vacant_info['salary_min'] = js_obj.get('items')[item].get('salary').get('from')
        except:
            vacant_info['salary_min'] = None

        try:
            vacant_info['salary_max'] = js_obj.get('items')[item].get('salary').get('to')
        except:
            vacant_info['salary_max'] = None

        try:
            vacant_info['salary_currency'] = js_obj.get('items')[item].get('salary').get('currency')
        except:
            vacant_info['salary_currency'] = None

        data_long = get_long_info(js_obj.get('items')[item].get('id'))
        js_obj_long = json.loads(data_long)

        vacant_info['experience'] = js_obj_long.get('experience').get('name')
        vacant_info['schedule'] = js_obj_long.get('schedule').get('name')
        vacant_info['employment'] = js_obj_long.get('employment').get('name')
        vacant_info['description'] = js_obj_long.get('description')
        vacant_info['key_skills'] = js_obj_long.get('key_skills')
        vacant_info['specializations'] = js_obj_long.get('specializations')
        vacant_info['employer'] = js_obj_long.get('employer')
        vacant_info['alternate_url'] = js_obj_long.get('alternate_url')
        vacant_info['professional_roles'] = js_obj_long.get('professional_roles')


    # print(mix_data)
    #
        try:
            parse_hh_easy.insert_one({'_id': int(vacant_info['id']),
                                  'name': vacant_info['name'],
                                  'area': vacant_info['area'],
                                  'salary_min': vacant_info['salary_min'],
                                 'salary_max': vacant_info['salary_min'],
                                'salary_currency': vacant_info['salary_currency'],
                                'experience': vacant_info['experience'],
                                'schedule': vacant_info['schedule'],
                                'description': vacant_info['description'],
                                      'key_skills' : vacant_info['key_skills'],

                                'employment': vacant_info['employment'],
                                'employer': vacant_info['employer'],
                                'professional_roles': vacant_info['professional_roles'],
                                'specializations': vacant_info['specializations']
                                  })

        except: dke

    return vacant_info






# Создаем список, в котором будут хранится ответы запроса к сервису API hh.ru
js_objs = []

# Считываем первые 2000 вакансий
for page in range(0, 20):

    # Преобразуем текст ответа запроса в словарь Python
    js_obj = json.loads(get_page(page))




    # Добавляем текущий ответ запроса в список
    js_objs.extend(js_obj["items"])




    # Проверка на последнюю страницу, если вакансий меньше 2000
    if (js_obj['pages'] - page) <= 1:
        break

    # Необязательная задержка, но чтобы не нагружать сервисы hh, оставим. 5 сек мы может подождать
    time.sleep(0.25)







print('Старницы поиска собраны')











#
#
#
# 'id': '49103113',
#  'premium': False,
#  'name': 'Инженер технической поддержки/HelpDesk (мобильные решения для бизнеса)',
#  'department': None,
#  'has_test': False,
#  'response_letter_required': False,
#  'area': {'id': '1', 'name': 'Москва', 'url': 'https://api.hh.ru/areas/1'},
#  'salary': {'from': 65000, 'to': 80000, 'currency': 'RUR', 'gross': True},
#  'type': {'id': 'open', 'name': 'Открытая'},
#  'address': {'city': 'Москва',
#   'street': 'Одесская улица',
#   'building': '2кА',
#   'description': None,
#   'lat': 55.664472,
#   'lng': 37.599238,
#   'raw': 'Москва, Одесская улица, 2кА',
#   'metro': {'station_name': 'Нахимовский проспект',
#    'line_name': 'Серпуховско-Тимирязевская',
#    'station_id': '9.87',
#    'line_id': '9',
#    'lat': 55.662379,
#    'lng': 37.605274},
#   'metro_stations': [{'station_name': 'Нахимовский проспект',
#     'line_name': 'Серпуховско-Тимирязевская',
#     'station_id': '9.87',
#     'line_id': '9',
#     'lat': 55.662379,
#     'lng': 37.605274}],
#   'id': '234556'},
#  'response_url': None,
#  'sort_point_distance': None,
#  'published_at': '2021-10-25T10:14:26+0300',
#  'created_at': '2021-10-25T10:14:26+0300',
#  'archived': False,
#  'apply_alternate_url': 'https://hh.ru/applicant/vacancy_response?vacancyId=49103113',
#  'insider_interview': None,
#  'url': 'https://api.hh.ru/vacancies/49103113?host=hh.ru',
#  'alternate_url': 'https://hh.ru/vacancy/49103113',
#  'relations': [],
#  'employer': {'id': '1193290',
#   'name': 'Сканпорт',
#   'url': 'https://api.hh.ru/employers/1193290',
#   'alternate_url': 'https://hh.ru/employer/1193290',
#   'logo_urls': {'90': 'https://hhcdn.ru/employer-logo/3245440.png',
#    '240': 'https://hhcdn.ru/employer-logo/3245441.png',
#    'original': 'https://hhcdn.ru/employer-logo-original/701081.png'},
#   'vacancies_url': 'https://api.hh.ru/vacancies?employer_id=1193290',
#   'trusted': True},
#  'snippet': {'requirement': 'Профессиональное образование в области информационных технологий (учащиеся ВУЗов также рассматриваются). Опыт работы в аналогичной должности в службе поддержки пользователей. ',
#   'responsibility': 'Принимать и обрабатывать запросы пользователей ПО DataMobile на портале Helpdesk. Оказывать помощь и консультации в рамках эксплуатации ПО. '},
#  'contacts': None,
#  'schedule': {'id': 'fullDay', 'name': 'Полный день'},
#  'working_days': [],
#  'working_time_intervals': [],
#  'working_time_modes': [],
#  'accept_temporary': False}
