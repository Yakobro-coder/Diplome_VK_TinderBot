import requests
import json
from selenium import webdriver
from random import randrange

from psql_database import requests_INSERT, requests_SELECT, requests_DELETE

from menu_template import like_dislike_menu
from menu_template import menu

import checking_info_user
import search_people
import collecting_photos


class ApiVk:

    def __init__(self, login, password, id_group):
        self.login = login
        self.password = password
        self.id_group = id_group

        self.url = 'https://api.vk.com/method/'

        self.group_token = None
        self.token = None

        self.server = None
        self.key = None
        self.ts = None

        self.params = {
            'access_token': self.token,
            'v': '5.131'
        }

        self.group_params = {
            'group_id': self.id_group
        }

        self.token = self.get_token()

        # self.set_long_poll_settings() - что бы задать настройки группы, включить лонгпул, и сообщения
        self.get_long_poll_server()

    def get_token(self):
        url_authorize = 'https://oauth.vk.com/authorize'
        url_blank = 'https://oauth.vk.com/blank.html'
        app_id = '7836316'
        params = {'client_id': app_id,
                  'redirect_uri': url_blank,
                  'scope': 'offline, groups, manage',
                  'response_type': 'token',
                  'v': '5.131'}

        url_send = requests.get(url_authorize, params=params).url

        driver = webdriver.Firefox()
        driver.get(url_send)

        # Для удобства сохраняем XPath формы авторизации
        # Заполняем форму авторизации
        username = '//*[@id="login_submit"]/div/div/input[6]'
        driver.find_element_by_xpath(username).send_keys([self.login])
        # time.sleep(1)

        password_form = '//*[@id="login_submit"]/div/div/input[7]'
        driver.find_element_by_xpath(password_form).send_keys([self.password])
        # time.sleep(1)

        press_enter = '//*[@id="install_allow"]'
        driver.find_element_by_xpath(press_enter).click()
        # time.sleep(3)

        # Если авторизации ранее уже прошла и подтверждени на доступ к правам не требуется, пропускаем этот шаг
        if url_blank not in driver.current_url:
            accepting_rules = '//*[@id="oauth_wrap_content"]/div[3]/div/div[1]/button[1]'
            driver.find_element_by_xpath(accepting_rules).click()
            # time.sleep(3)

        result_url = driver.current_url
        # time.sleep(1)

        # Получем токен пользователя из урла
        self.token = result_url[result_url.find('=', 0) + 1:result_url.find('&', 0)]

        # Запрос для получения токена группы
        url_send2 = requests.get(url_authorize, params={**self.params, **{'client_id': app_id,
                                                                          'group_ids': str(self.id_group),
                                                                          'display': 'page',
                                                                          'redirect_uri': url_blank,
                                                                          'scope': 'manage, messages',
                                                                          'response_type': 'token'
                                                                          }}).url
        driver.get(url_send2)
        press_enter = '/html/body/div/div/div/div[3]/div/div[1]/button[1]'
        driver.find_element_by_xpath(press_enter).click()

        result_url = driver.current_url

        # Получаем токен групп
        self.group_token = result_url.split('=')[2]
        # Обновляем параметры токеном пользователя
        self.params['access_token'] = self.token

        driver.close()

        return self.token

    def get_long_poll_server(self):
        response = requests.get(self.url + 'groups.getLongPollServer',
                                params={**self.params, **self.group_params}).json()

        self.server = response['response'].get('server')
        self.key = response['response'].get('key')
        self.ts = response['response'].get('ts')

        self.callback_server()

    def callback_server(self):
        while True:
            url = self.server
            params = {'key': self.key,
                      'ts': self.ts,
                      'act': 'a_check',
                      'wait': 25}

            response = requests.get(url, params={**self.params, **self.group_params, **params}).json()
            print('~' * 30, 'callback_server', '~' * 30, 1)
            print(response)
            print('~' * 30, 'callback_server', '~' * 30, 2)
            print()

            self.ts = response.get('ts')

            if 'failed' in response:
                self.get_long_poll_server()

            if len(response['updates']) > 0 and response['updates'][0]['type'] == 'message_new':
                info_object = response['updates'][0]['object']['message']
                user_id = info_object['from_id']
                body_msg = info_object['text']

                if body_msg == 'Начать':
                    hi_text = """Приветствую, я БОТ по поиску собеседника!
                        """
                    text_message = 'Для кого вы ищите пару? Укажите id(толко цифры) пользователя ' \
                                   'или его короткое имя.'
                    self.send_message(user_id, hi_text + text_message, menu.menu)

                if body_msg == 'Заново':
                    hi_text = """Все настройки поиска и данные сброшены. 
                    Начнём сначала.
                    """
                    text_message = 'Для кого вы ищите пару? Укажите id(толко цифры) пользователя ' \
                                   'или его короткое имя.'
                    requests_DELETE.delete_from_bd(user_id)
                    self.send_message(user_id, hi_text + text_message, menu.menu)

                elif body_msg == 'Для себя!':
                    json_user_info = self.get_info_user(user_id)
                    json_user_info = json.dumps(json_user_info)
                    requests_INSERT.insert_user_info(user_id, json_user_info)

                else:  # Любой другой ввод
                    if body_msg != 'Dislike!' and body_msg != 'Like!' and len(requests_SELECT.check_info(user_id)) == 0:
                        json_user_info = self.get_info_user(user_id, body_msg)
                        if isinstance(json_user_info, str):
                            self.send_message(user_id, json_user_info)
                            requests_DELETE.delete_from_bd(user_id)
                            continue
                        json_user_info = json.dumps(json_user_info)
                        requests_INSERT.insert_user_info(user_id,
                                                         json_user_info,
                                                         body_msg)

                # Задаём дату рождения и город прибвания из сообщения
                if len(requests_SELECT.check_info(user_id)) != 0 and body_msg != 'Начать':
                    json_user_info = requests_SELECT.json_info(user_id)[1]
                    if isinstance(json_user_info, str):
                        self.send_message(user_id, json_user_info)
                        requests_DELETE.delete_from_bd(user_id)
                    elif None in json_user_info.values() or True in json_user_info.values():
                        if json_user_info['bdate'] is True:
                            json_user_info['bdate'] = int(body_msg)
                        elif json_user_info['bdate'] is None:
                            self.send_message(user_id, text_message='Укажите цифрой, ваш возраст.')
                            json_user_info['bdate'] = True

                        if json_user_info['bdate'] is not None and json_user_info['bdate'] is not True:
                            if json_user_info['city'] is True:
                                json_user_info['city'] = body_msg
                            elif json_user_info['city'] is None:
                                self.send_message(user_id, text_message='Укажите ваш город пребывания.')
                                json_user_info['city'] = True

                        json_user_info = json.dumps(json_user_info)
                        requests_INSERT.update_json(user_id, json_user_info)

                if body_msg == 'Like!':
                    people_id = requests_SELECT.select_found_people(user_id)
                    requests_INSERT.insert_like(user_id, people_id)

                if body_msg == 'Dislike!':
                    people_id = requests_SELECT.select_found_people(user_id)
                    requests_INSERT.insert_dislike(user_id, people_id)

                # Выводит ссылку и 3 фото подходящих людей, если есть вся необходимая инфа о user для поиска
                info = requests_SELECT.json_info(user_id)
                if len(info[1]) != 0 and body_msg != 'Начать':
                    if True not in info[1].values() and None not in info[1].values():
                        # Выполняем поиск людей по параметрам пользователя если в базе уже нету людей со статусом NULL
                        if requests_SELECT.select_found_people(user_id) is None:
                            search_people.search_people(self.token, user_id, info[1])
                            self.send_message(user_id, 'Если вы захотите начать поиск сзанова, напишите "Заново".')
                        people_id = requests_SELECT.select_found_people(user_id)
                        url_photo = collecting_photos.collecting_photos(self.token, people_id)
                        msg = f'https://vk.com/id{people_id}'
                        if people_id is None:
                            msg = 'Список подходящих вам людей закончился :('

                        self.send_message(user_id, msg,
                                          like_dislike_menu.like_dis_menu,
                                          photo=url_photo)

    def send_message(self, user_id, text_message, menu_param='', photo=''):
        params = {'access_token': self.group_token,
                  'v': '5.131',
                  'message': text_message,
                  'attachment': photo,
                  'peer_ids': user_id,
                  'random_id': randrange(10 ** 7),
                  'keyboard': menu_param
                  }
        response = requests.get(self.url + 'messages.send', params={**self.group_params, **params}).json()

        print(response)

    def get_info_user(self, user_id, search_user=None):
        params = {
            'user_ids': user_id,
            'fields': 'bdate, sex, city, relation'
        }

        if search_user is not None:
            params = {
                'user_ids': search_user,
                'fields': 'bdate, sex, city, relation'
            }

        response = requests.get(self.url + 'users.get', params={**self.params, **params}).json()
        result = checking_info_user.InfoUser()
        return result.info_user(response)

    # get setting group получить параметры группы
    def get_long_poll_settings(self):
        response = requests.get(self.url + 'groups.getLongPollSettings',
                                params={**self.params, **self.group_params}).json()

    # enable long poll in group, enable check received message in group
    def set_long_poll_settings(self):
        set_params = {
            'enabled': 1,
            'message_new': 1
        }
        response = requests.get(self.url + 'groups.setLongPollSettings',
                                params={**self.group_params, **set_params}).json()


if __name__ == '__main__':
    # Логин:пас админа группы, id group
    ApiVk('loginAdminGroup@mail.ru', 'PasswordAdminGroup', 'idGroup')
