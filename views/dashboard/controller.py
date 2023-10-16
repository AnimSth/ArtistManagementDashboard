from db import db_config
import psycopg2
# from flask import jsonify
def get_users():
    user_list = []

    with psycopg2.connect(db_config) as connection:
        with connection.cursor() as cursor:
            select_all_query = "SELECT id, first_name, last_name, email FROM users;"
            cursor.execute(select_all_query)

            cursor.itersize = 100

            for row in cursor:
                user_dict = {
                    'id': row[0],
                    'first_name': row[1],
                    'last_name': row[2],
                    'email': row[3],
                }
                user_list.append(user_dict)

    return user_list


def fetch_userId(id:int):
    with psycopg2.connect(db_config) as connection, connection.cursor() as cursor:
        select_query = "SELECT * FROM users WHERE id = %s;"
        cursor.execute(select_query, (id,))
        user_data = cursor.fetchone()
        column_names = [desc[0] for desc in cursor.description] if user_data else []
    user_data_dict = dict(zip(column_names, user_data))
    return user_data_dict
