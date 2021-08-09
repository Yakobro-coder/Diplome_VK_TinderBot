import requests


def collecting_photos(token, user_id):
    url = 'https://api.vk.com/method/'
    params = {'access_token': token,
              'v': '5.131',
              'owner_id': user_id,
              'album_id': 'profile',
              'extended': 1,
              'photo_sizes': 1
              }
    # Получаем все самые качественные(большие) фото с аватарок людей из нашего поиска
    resp = requests.get(url + 'photos.get', params=params).json()

    resp = resp['response']['items']
    # делаем список списков [[кол-во лайкво, ссылка на фото1], [кол-во лайкво, ссылка на фото2], [...]]
    user_photo_base = [[info['likes']['count'], f"photo{user_id}_{info['id']}"] for info in resp]
    user_photo_base.sort()

    user_photo_base = user_photo_base[-1:-4:-1]

    if len(user_photo_base) == 3:
        return f'{user_photo_base[0][1]},{user_photo_base[1][1]},{user_photo_base[2][1]}'
    elif len(user_photo_base) == 2:
        return f'{user_photo_base[0][1]},{user_photo_base[1][1]}'
    elif len(user_photo_base) == 1:
        return f'{user_photo_base[0][1]}'
