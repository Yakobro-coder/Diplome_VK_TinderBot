

def create_table(connection):
    connection.execute('create table if not exists users_info('
                       'id_vk integer primary key,'
                       'id_search integer not null,'
                       'json_info jsonb'
                       ');')

    connection.execute('create table if not exists found_people('
                       'id_vk integer references users_info(id_vk),'
                       'id_people integer not null,'
                       'check_status boolean,'
                       'constraint found_people_pk primary key (id_vk, id_people)'
                       ');')
