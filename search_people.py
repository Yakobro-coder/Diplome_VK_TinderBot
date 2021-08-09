import requests
from psql_database import requests_INSERT


# Поиск  людей по необходимым параметрам
def search_people(token, user_id, base_info):
    city = base_info['city']
    if int(base_info['sex']) == 2:
        sex = 1
    else:
        sex = 2

    age_from = int(base_info['bdate']) - 1
    age_to = int(base_info['bdate']) + 1

    status = 6

    url = 'https://api.vk.com/method/'

    params = {'access_token': token,
              'v': '5.131',
              'count': 1000,
              'hometown': city,
              'sex': sex,
              'status': status,
              'age_from': age_from,
              'age_to': age_to,
              'has_photo': 1
              }

    search = requests.get(url + 'users.search', params).json()

    # Если страница не закрыта, добавить в список -  id(человека)
    people_base = [user_id['id'] for user_id in search['response']['items'] if user_id.get('is_closed') is False]

    # Записываем в БД id пользователя бота, и id подходящего человека
    for id_people in people_base:
        requests_INSERT.insert_found_people(user_id, id_people)
