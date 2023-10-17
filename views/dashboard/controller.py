from db import db_config
import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify, flash


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

def fetch_artistId(id:int):
    with psycopg2.connect(db_config) as connection, connection.cursor() as cursor:
        select_query = "SELECT * FROM artist WHERE id = %s;"
        cursor.execute(select_query, (id,))
        artist_data = cursor.fetchone()
        column_names = [desc[0] for desc in cursor.description] if artist_data else []
    artist_data_dict = dict(zip(column_names, artist_data))
    return artist_data_dict
def user_registration(user_info: dict):
    try:
        with psycopg2.connect(db_config) as connection, connection.cursor() as cursor:
            select_query = "SELECT 1 FROM users WHERE email = %s;"
            cursor.execute(select_query, (user_info.get('email'),))
            user = cursor.fetchone()

            if not user:
                user_info['password'] = generate_password_hash(user_info.get("password"))

                insert_query = """
                    INSERT INTO users (first_name, last_name, email, dob, phone, address, gender, password)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
                """
                cursor.execute(
                    insert_query,
                    (
                        user_info.get('first_name'),
                        user_info.get('last_name'),
                        user_info.get('email'),
                        user_info.get('dob'),
                        user_info.get('phonenumber'),
                        user_info.get('address'),
                        user_info.get('gender'),
                        user_info.get('password'),
                    ),
                )
                connection.commit()
                flash('Users registered successfully.', 'success')
                return {"success": True, "message": 'User added successfully.'}

            return {"success": False, "message": 'User email exists already. Please Login.'}

    except Exception as e:
        return {"success": False, "message": "User couldn't be registered", "exception": str(e)}

def edit_user(user_info: dict):
    try:
        with psycopg2.connect(db_config) as connection, connection.cursor() as cursor:
            # Check if the user exists based on their ID
            select_query = "SELECT 1 FROM users WHERE id = %s;"
            cursor.execute(select_query, (user_info.get('id'),))
            user = cursor.fetchone()

            if user is not None:
                # Update user information
                update_query = """
                    UPDATE users
                    SET first_name = %s, last_name = %s, email = %s, dob = %s,
                        phone = %s, address = %s, gender = %s,
                        updated_at = current_timestamp
                    WHERE id = %s;
                """
                cursor.execute(
                    update_query,
                    (
                        user_info.get('first_name'),
                        user_info.get('last_name'),
                        user_info.get('email'),
                        user_info.get('dob'),
                        user_info.get('phonenumber'),
                        user_info.get('address'),
                        user_info.get('gender'),
                        user_info.get('id'),
                    ),
                )
                connection.commit()
                flash('Admin user updated successfully.', 'success')
                return {"success": True, "message": 'User updated successfully.'}
            else:
                return {"success": False, "message": 'User not found.'}

    except Exception as e:
        return {"success": False, "message": "User couldn't be updated", "exception": str(e)}

def delete_user(user_id: int):
    try:
        with psycopg2.connect(db_config) as connection, connection.cursor() as cursor:
            # Check if the user exists based on their ID
            select_query = "SELECT 1 FROM users WHERE id = %s;"
            cursor.execute(select_query, (user_id,))
            user = cursor.fetchone()

            if user:
                # Delete the user
                delete_query = "DELETE FROM users WHERE id = %s;"
                cursor.execute(delete_query, (user_id,))
                connection.commit()
                flash('User deleted successfully.', 'success')
                return {"success": True, "message": 'User deleted successfully.'}
            else:
                return {"success": False, "message": 'User not found.'}

    except Exception as e:
        return {"success": False, "message": "User couldn't be deleted", "exception": str(e)}

def artist_registration(artist_info: dict):
    try:
        with psycopg2.connect(db_config) as connection, connection.cursor() as cursor:
            select_query = "SELECT 1 FROM artist WHERE name = %s;"
            cursor.execute(select_query, (artist_info.get('name'),))
            user = cursor.fetchone()

            if user is None:
                insert_query = """
                    INSERT INTO artist (name, dob, gender, address, first_release_year, no_of_albums_released)
                    VALUES (%s, %s, %s, %s, %s, %s);
                """
                cursor.execute(
                    insert_query,
                    (
                        artist_info.get('name'),
                        artist_info.get('dob'),
                        artist_info.get('gender'),
                        artist_info.get('address'),
                        artist_info.get('first_release_year'),
                        artist_info.get('no_of_albums_released'),
                    ),
                )

                connection.commit()
                flash('Artist registered successfully.', 'success')
                return {"success": True, "message": 'Artist added successfully.'}

            return {"success": False, "message": 'Artist name exists already. Please user another name.'}

    except Exception as e:
        return {"success": False, "message": "Artist couldn't be registered", "exception": str(e)}

def artist_registrationWithNoflash(artist_info: dict):
    try:
        with psycopg2.connect(db_config) as connection, connection.cursor() as cursor:
            select_query = "SELECT 1 FROM artist WHERE name = %s;"
            cursor.execute(select_query, (artist_info.get('name'),))
            user = cursor.fetchone()

            if user is None:
                insert_query = """
                    INSERT INTO artist (name, dob, gender, address, first_release_year, no_of_albums_released)
                    VALUES (%s, %s, %s, %s, %s, %s);
                """
                cursor.execute(
                    insert_query,
                    (
                        artist_info.get('name'),
                        artist_info.get('dob'),
                        artist_info.get('gender'),
                        artist_info.get('address'),
                        artist_info.get('first_release_year'),
                        artist_info.get('no_of_albums_released'),
                    ),
                )

                connection.commit()
                return {"success": True, "message": 'Artist added successfully.'}

            return {"success": False, "message": 'Artist name exists already. Please user another name.'}

    except Exception as e:
        return {"success": False, "message": "Artist couldn't be registered", "exception": str(e)}

def edit_artist(artist_info: dict):
    try:
        with psycopg2.connect(db_config) as connection, connection.cursor() as cursor:
            # Check if the artist exists based on their ID
            select_query = "SELECT 1 FROM artist WHERE id = %s;"
            cursor.execute(select_query, (artist_info.get('id'),))
            artist = cursor.fetchone()

            if artist is not None:
                # Update artist information
                update_query = """
                    UPDATE artist
                    SET name = %s, dob = %s, gender = %s, address = %s,
                        first_release_year = %s, no_of_albums_released = %s,
                        updated_at = current_timestamp
                    WHERE id = %s;
                """
                cursor.execute(
                    update_query,
                    (
                        artist_info.get('name'),
                        artist_info.get('dob'),
                        artist_info.get('gender'),
                        artist_info.get('address'),
                        artist_info.get('first_release_year'),
                        artist_info.get('no_of_albums_released'),
                        artist_info.get('id'),
                    ),
                )
                connection.commit()
                flash('Artist information updated successfully.', 'success')
                return {"success": True, "message": 'Artist information updated successfully.'}
            else:
                return {"success": False, "message": 'Artist not found.'}

    except Exception as e:
        return {"success": False, "message": "Artist information couldn't be updated", "exception": str(e)}

def delete_artist(user_id: int):
    try:
        with psycopg2.connect(db_config) as connection, connection.cursor() as cursor:
            # Check if the user exists based on their ID
            select_query = "SELECT 1 FROM artist WHERE id = %s;"
            cursor.execute(select_query, (user_id,))
            user = cursor.fetchone()

            if user:
                # Delete the user
                delete_query = "DELETE FROM artist WHERE id = %s;"
                cursor.execute(delete_query, (user_id,))
                connection.commit()
                flash('Artist deleted successfully.', 'success')
                return {"success": True, "message": 'Artist deleted successfully.'}
            else:
                return {"success": False, "message": 'Artist not found.'}

    except Exception as e:
        return {"success": False, "message": "Artist couldn't be deleted", "exception": str(e)}

def allowed_file(filename):
    # Check if the file has a CSV extension
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'csv'