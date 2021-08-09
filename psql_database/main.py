import sqlalchemy
import requests_CREATE


# Запустить, для создания таблиц БД
if __name__ == '__main__':
    db = 'postgresql://diplome2:qwer@localhost:5432/vkinder_base'
    engine = sqlalchemy.create_engine(db)
    connection = engine.connect()

    requests_CREATE.create_table(connection)
