from ..model import LoginForm
from flask import (Blueprint, 
	render_template, 
	request, url_for, 
	redirect,session,
	flash,
	jsonify,
	Response)
from db import db_config
import psycopg2
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash

#-------Wrapper----------

def admin_required(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if not session.get('authenticated_verification'):
                return redirect('/login')
            return f(*args, **kwargs)
        return wrapped
    return wrapper

def logged_in(f):
    def wrapped(*args, **kwargs):
        if session.get('authenticated_verification'):
            return redirect('/')
        return f(*args, **kwargs)
    return wrapped


def user_validation(user_info:dict):
    try:
        user = fetch_user(user_info.get('email'))
        if user:
            if check_password_hash(user.get('password'), user_info.get('password')):
                session['user_id'] = user.get('id') 
                session['authenticated_verification'] = True
                session['username'] =f"{user.get('first_name')} {user.get('last_name')}"  
        
                # flash('Login successful', 'success')
                return {"success":True,"message":'User found.'}
            return {"success":False,"message":'Password invalid. Please try again.'}
        return {"success":False,"message":'User not found. Please register.'}
    except Exception as e:
        return {"success":False,"message":"User not found. Please try again.","exception":e}

def fetch_user(email:str):
    with psycopg2.connect(db_config) as connection, connection.cursor() as cursor:
        select_query = "SELECT first_name, last_name, password FROM admin WHERE email = %s;"
        cursor.execute(select_query, (email,))
        user_data = cursor.fetchone()
        column_names = [desc[0] for desc in cursor.description] if user_data else []
    user_data_dict = dict(zip(column_names, user_data))
    return user_data_dict

def admin_registration(user_info: dict):
    try:
        with psycopg2.connect(db_config) as connection, connection.cursor() as cursor:
            select_query = "SELECT 1 FROM admin WHERE email = %s;"
            cursor.execute(select_query, (user_info.get('email'),))
            user = cursor.fetchone()

            if user is None:
                user_info['password'] = generate_password_hash(user_info.get("password"))

                insert_query = """
                    INSERT INTO admin (first_name, last_name, email, dob, phone, address, gender, password)
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
                flash('Admin registered successfully.', 'success')
                return {"success": True, "message": 'User added successfully.'}

            return {"success": False, "message": 'User email exists already. Please Login.'}

    except Exception as e:
        return {"success": False, "message": "User couldn't be registered", "exception": str(e)}

