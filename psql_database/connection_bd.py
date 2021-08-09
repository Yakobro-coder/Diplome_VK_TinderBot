import sqlalchemy


def connect():
    db = 'postgresql://diplome2:qwer@localhost:5432/vkinder_base'
    engine = sqlalchemy.create_engine(db)
    connection = engine.connect()

    return connection
