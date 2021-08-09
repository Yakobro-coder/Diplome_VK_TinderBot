from psql_database import connection_bd


def delete_from_bd(user_id, connection=connection_bd.connect()):
    connection.execute("""DELETE FROM found_people
WHERE id_vk = %s;""", (user_id,))

    connection.execute("""DELETE FROM users_info
    WHERE id_vk = %s;""", (user_id,))
