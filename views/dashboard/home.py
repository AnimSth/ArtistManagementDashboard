from views.authentication.controller import admin_required
from flask import (Blueprint, 
	render_template, 
	request, url_for, 
	redirect,session,
	flash,
	jsonify,
	Response)

from ..model import LoginForm
from .controller import get_users,fetch_userId
import psycopg2
from db import db_config

dash = Blueprint('dashboard', __name__,static_url_path='/static',static_folder='./static',template_folder="./templates")

@dash.route('/',methods= ["GET"])
@admin_required()
def home():
    print("heloo")
    users = get_users()
    print(users)
    return render_template('index.html', users = users, admin_name=session.get("username"))


@dash.route('/UserList')
@admin_required()
def show_usersList():
    return render_template('user_list.html')

@dash.route('/users_data', methods=['POST'])
@admin_required()
def user_data():
    columns = ['id', 'first_name', 'last_name', 'email']

    draw = request.form.get('draw')
    start = request.form.get('start')
    length = request.form.get('length')
    search_value = request.form.get('search[value]')

    # Open a database connection
    with psycopg2.connect(db_config) as connection, connection.cursor() as cursor:
        base_query = f"SELECT {', '.join(columns)} FROM users"

        if search_value:
            search_query = f"{base_query} WHERE email ILIKE '%{search_value}%'"
        else:
            search_query = base_query

        cursor.execute(search_query)
        total_records = len(cursor.fetchall())

        order_column_index = int(request.form.get('order[0][column]'))
        order_column = columns[order_column_index]
        order_dir = request.form.get('order[0][dir]')
        order_query = f"{search_query} ORDER BY {order_column} {'DESC' if order_dir == 'desc' else 'ASC'}"

        paginated_query = f"{order_query} LIMIT {length} OFFSET {start}"

        cursor.execute(paginated_query)
        data = [dict(zip(columns, row)) for row in cursor]

        response = {
            'draw': draw,
            'recordsTotal': total_records,
            'recordsFiltered': total_records,
            'data': data
        }

    return jsonify(response)

@dash.route('/userdata/<id>', methods=['POST', 'GET'])
@admin_required()
def user_D(id):
	user = fetch_userId(id)
	print(user)
	return render_template('register_admin.html',submitted_data=user)
     

