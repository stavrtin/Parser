import os
from dotenv import load_dotenv
from django.shortcuts import render
import requests
import json


def home(request):
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)

    # Ваши учетные данные API
    api_key = os.getenv('API_KEY')
    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')

    # Конечная точка API
    endpoint = "https://api.foursquare.com/v3/places/search"

    headers = {
        "Accept": "application/json",
        "Authorization": api_key
    }

    city = ''
    category = ''
    limit = ''

    # Проверяем, был ли запрос методом POST
    if request.method == 'POST':
        # Извлекаем значения из полей формы
        city = request.POST.get('city')
        category = request.POST.get('category')
        limit = request.POST.get('limit')

    # Определение параметров для запроса API
    params = {
        "near": city,
        "query": category,
        'limit': limit
    }

    # Отправка запроса API и получение ответа
    response = requests.get(endpoint, params=params, headers=headers)

    # Проверка успешности запроса API
    venues = []
    if response.status_code == 200:
        print("Успешный запрос API!")
        data = json.loads(response.text)
        venues = data.get("results", [])

    else:
        print("Запрос API завершился неудачей с кодом состояния:", response.status_code)
        print(response.text)

        # Создаем список словарей для передачи в шаблон
    results = []
    for venue in venues:
        results.append({
            "name": venue["name"],
            "address": venue["location"].get("address", "Нет адреса"),
            "region": venue['location'].get('region', "Нет региона"),
            "latitude": venue['geocodes']['main'].get('latitude', "Нет данных"),
            "longitude": venue['geocodes']['main'].get('longitude', "Нет данных"),
        })


    # Передаем значения в шаблон
    return render(request, 'home.html', {
        'city': city,
        'category': category,
        'limit': limit,
        'results': results,  # Передаем список словарей
    })




#

#

#
# # Определение параметров для запроса API
# city = input("Введите название города: ")
# category = input("Введите категорию: ")
# limit = input("Введите макс.: ")
#
# params = {
#     # "client_id": client_id,
#     # "client_secret": client_secret,
#     "near": city,
#     "query": category,
#     'limit':limit
# }
#
#
#
# # Отправка запроса API и получение ответа
# response = requests.get(endpoint, params=params,headers=headers)
#
# # Проверка успешности запроса API
# if response.status_code == 200:
#     print("Успешный запрос API!")
#     data = json.loads(response.text)
#     venues = data["results"]
#     for venue in venues:
#         print("Название:", venue["name"])
#         print("Адрес:", venue["location"]["address"])
#         print("region:", venue['location']['region'])
#         print("latitude:", venue['geocodes']['main']['latitude'], "longitude", venue['geocodes']['main']['longitude'])
#         print("\n")
# else:
#     print("Запрос API завершился неудачей с кодом состояния:", response.status_code)
#     print(response.text)