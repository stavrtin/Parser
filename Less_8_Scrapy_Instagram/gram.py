import scrapy
from scrapy.http import HtmlResponse
import re
import json
from gram_prj.items import GramPrjItem
from pprint import pprint



class GramSpider(scrapy.Spider):
    name = 'gram'
    allowed_domains = ['instagram.com']
    start_urls = ['http://instagram.com/']
    inst_login_links = 'https://www.instagram.com/accounts/login/ajax/'

    inst_login = 'Onliskill_udm'   # Qw123456789
    inst_pwd = '#PWD_INSTAGRAM_BROWSER:10:1634577477:AWdQAK0AEOF+wFwWVYjoEuu8uCHn+Pabck9vUxQlFS3/o3VdiZCGuEm4HaF+MLP9EwSytUXe+VNGZWVqv/Pz+z14vr8gT4dClBa6OPYXzPbHCHcU0fUqrO731Bcf4OCxjIcxB4lurkTpWrZPz+Ir'


    users_for_parse = ['roby_dik', 'gorbunov_andruha']

    api_url = f'https://i.instagram.com/api/v1/friendships/'
    followers = []


    def parse(self, response: HtmlResponse):
        '''метод авторизации для входа на инстаграмм'''
        csrf = self.fetch_csrf_token(response.text)
        yield scrapy.FormRequest(
            self.inst_login_links,
            method='POST',
            callback=self.login,
            formdata={'username': self.inst_login,
                      'enc_password': self.inst_pwd},
            headers={'X-CSRFToken': csrf}

        )

    def login(self, response: HtmlResponse):

       '''проверяем - авторизовались ли мы?  '''
       j_data = response.json()
       if j_data['authenticated']:
           for user_for_parse in self.users_for_parse:
               yield response.follow(
                   f'/{user_for_parse}',
                   callback=self.user_parse,
                   cb_kwargs={'username': user_for_parse}
               )

    def user_parse(self, response: HtmlResponse, username):
        '''формируем первый API_запрос для старта прокрутки страницы подписчиков и подписок'''

        user_id = self.fetch_user_id(response.text, username)

        ''' формируем ссылку для захода на ПОДПИСЧИКИ '''
        url_followers_first_page = f'{self.api_url}{user_id}/followers/?count=12&search_surface=follow_list_page' # сформируем ссылку для

        yield response.follow(url_followers_first_page,
                              callback=self.followers_list_parse,
                              cb_kwargs={'username': username,
                                          'user_id': user_id},
                              headers={'User-Agent': 'Instagram 155.0.0.37.107'}
                              )

        ''' формируем ссылку для захода на ПОДПИСКИ '''
        url_following_first_page = f'{self.api_url}{user_id}/following/?count=12'
        yield response.follow(url_following_first_page,
                              callback=self.following_list_parse,
                              cb_kwargs={'username': username,
                                         'user_id': user_id},
                              headers={'User-Agent': 'Instagram 155.0.0.37.107'}
                              )

    def followers_list_parse(self, response: HtmlResponse, username, user_id):
        j_data = response.json()

        if j_data.get('big_list'):
            max_id = j_data.get('next_max_id')

            url_followers_next_page = f'{self.api_url}{user_id}/followers/?count=12&max_id={max_id}&search_surface=follow_list_page'

            ''' рекурсивно проходим по ссылкам'''
            yield response.follow(url_followers_next_page, callback=self.followers_list_parse,
                                              cb_kwargs={'username': username,
                                              'user_id': user_id},
                                              headers={'User-Agent': 'Instagram 155.0.0.37.107'})

            '''Собираю всех подписчиков в список и далее прогоняю его через item в pipline и далее в БД'''
            follower_users_list = j_data.get('users')
            for follower in follower_users_list:

                item = GramPrjItem(
                    follower_user_id=follower.get('pk'),  # собираем данные
                    follower_username=follower.get('username'),
                    follower_full_name=follower.get('full_name'),
                    photo=follower.get('profile_pic_url'),
                    follower_user_data=follower,
                    username=username
                )
                yield item

    def following_list_parse(self, response: HtmlResponse, username, user_id):
        j_data = response.json()

        if j_data.get('big_list'):
            max_id = j_data.get('next_max_id')

            url_following_next_page = f'{self.api_url}{user_id}/following/?count=12&max_id={max_id}'

            ''' рекурсивно проходим по ссылкам'''
            yield response.follow(url_following_next_page, callback=self.following_list_parse,
                                              cb_kwargs={'username': username,
                                              'user_id': user_id},
                                              headers={'User-Agent': 'Instagram 155.0.0.37.107'})

            '''Собираю всех подписчиков в список и далее прогоняю его через item в pipline и далее в БД'''
            followinger_users_list = j_data.get('users')
            for following in followinger_users_list:

                item = GramPrjItem(
                    followinger_user_id=following.get('pk'),  # собираем данные
                    followinger_username=following.get('username'),
                    followinger_full_name=following.get('full_name'),
                    photo=following.get('profile_pic_url'),
                    followinger_user_data=following,
                    username=username
                )
                yield item

    def fetch_csrf_token(self, text):
        '''выковыриваем со страницы авторизации токен хеширования пароля'''
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    def fetch_user_id(self, text, username):
        '''выковыриваем id со страницы пользователя'''
        matched = re.search(
            '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
        ).group()
        return json.loads(matched).get('id')