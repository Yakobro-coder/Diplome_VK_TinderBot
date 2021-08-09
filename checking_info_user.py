import datetime


# Проверка всех необходимых данных о пользователе, на их наличие и соответствие нужн.формату
class InfoUser:
    def __init__(self):
        self.id = None
        self.first_name = None
        self.last_name = None
        self.sex = None
        self.bdate = None
        self.city = None
        self.relation = None

    def info_user(self, get_info_user):
        if 'error' in get_info_user:
            if get_info_user.get('error').get('error_code') == 113:
                return 'Вы ввели некоректный id(короткое имя) пользователя.\n' \
                       'Попробуйте ещё раз...'

        elif 'deactivated' in get_info_user['response'][0] and get_info_user['response'][0].get('deactivated') == 'deleted':
            return 'Аккаунт данного пользователя удалён. Подбор не возможен, укажите id другого аккаунта.'

        elif 'error' not in get_info_user:
            self.id = get_info_user['response'][0]['id']
            self.first_name = get_info_user['response'][0]['first_name']
            self.last_name = get_info_user['response'][0]['last_name']
            self.sex = get_info_user['response'][0]['sex']

            # Если дата рождения указана, и указана полностью, то {dateNow(год) - год рождения} else дата = None
            if 'bdate' not in get_info_user['response'][0]:
                pass
            else:
                if len(get_info_user['response'][0]['bdate'].split('.')) > 2:
                    self.bdate = int(datetime.datetime.now().strftime('%Y')) - int(get_info_user['response'][0]['bdate'].split('.')[2])

            if 'relation' not in get_info_user['response'][0]:
                pass
            else:
                self.relation = get_info_user['response'][0]['relation']

            if 'city' not in get_info_user['response'][0]:
                pass
            else:
                self.city = get_info_user['response'][0]['city']['title']

            if self.relation is None:
                self.relation = 'Not specified'

        result = {'id': str(self.id),
                  'bdate': self.bdate,
                  'sex': str(self.sex),
                  'city': self.city,
                  'relation': self.relation}

        return result
