from psql_database import connection_bd


def select_found_people(id_user, connection=connection_bd.connect()):
    try:
        id_people = connection.execute("""SELECT id_people FROM found_people f
            WHERE f.id_vk = %s and f.check_status is NULL;""", (id_user,)
                                       ).fetchmany(1)[0][0]
    except IndexError:
        id_people = None
    return id_people


def json_info(id_user, connection=connection_bd.connect()):
    try:
        json_user_info = connection.execute("""SELECT id_search,json_info FROM users_info u
            WHERE u.id_vk = %s;""", (id_user,)).fetchall()[0]
    except IndexError:
        json_user_info = [[], []]
    return json_user_info


def check_info(id_user, connection=connection_bd.connect()):
    return connection.execute("""SELECT id_vk FROM users_info
WHERE id_vk = %s;""", (id_user,)).fetchall()
