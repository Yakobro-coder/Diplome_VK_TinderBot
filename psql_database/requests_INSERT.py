from psql_database import connection_bd
from sqlalchemy import exc


def insert_user_info(user_id, json_info, id_search=None, connection=connection_bd.connect()):
    if id_search is None:
        id_search = user_id
    try:
        connection.execute('INSERT INTO users_info(id_vk, id_search, json_info)'
                           'VALUES(%s, %s, %s);', (user_id, id_search, json_info,))
    except exc.SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)


def insert_found_people(user_id, id_people, connection=connection_bd.connect()):
    try:
        connection.execute('INSERT INTO found_people(id_vk, id_people, check_status)'
                           'VALUES(%s, %s, NULL::boolean);', (user_id, id_people,))
    except exc.SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)


def insert_like(user_id, id_people, connection=connection_bd.connect()):
    connection.execute("""UPDATE found_people
SET check_status = TRUE
WHERE id_vk = %s AND id_people = %s;""", (user_id, id_people,))


def insert_dislike(user_id, id_people, connection=connection_bd.connect()):
    connection.execute("""UPDATE found_people
SET check_status = FALSE
WHERE id_vk = %s AND id_people = %s;""", (user_id, id_people,))


def update_json(user_id, json_info, id_search=None, connection=connection_bd.connect()):
    if id_search is None:
        id_search = user_id
    connection.execute("""UPDATE users_info
SET json_info = %s, id_search = %s
WHERE id_vk = %s;""", (json_info, id_search, user_id))
