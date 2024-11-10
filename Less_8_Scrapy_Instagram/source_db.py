from pymongo import MongoClient
from pprint import pprint

# 'roby_dik'
# 'gorbunov_andruha'

client = MongoClient('localhost', 27017)
db = client['Instagram']
name_s = input('Укажите имя пользователя: ')
collection = db.name_s
if name_s in db.list_collection_names():
    following = db.get_collection(name_s).find({'username': name_s}, {'followinger_full_name': 1})
    count = 0
    for i in following:
        if i.get('followinger_full_name'):
            pprint(i.get('followinger_full_name'))
            count += 1

    print(f'У пользователя {name_s} обнаружено {count} подписок')
    print('~~~'*20)

    following = db.get_collection(name_s).find({'username': name_s}, {'follower_full_name': 1})
    count = 0
    for i in following:
        if i.get('follower_full_name'):
            pprint(i.get('follower_full_name'))
            count += 1

    print(f'У пользователя {name_s} обнаружено {count} подписчиков.')
    print('~~~'*20)

else: print(f'Данных о пользователе  {name_s} пока нет в базе')



