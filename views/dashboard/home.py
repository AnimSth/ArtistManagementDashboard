from views.authentication.controller import admin_required
from flask import (Blueprint, 
	render_template, 
	request, url_for, 
	redirect,session,
	flash,
	jsonify,
	Response)

from ..model import LoginForm,registerAdminForm,registerArtistForm, registerMusicForm
from .controller import *
import psycopg2
from db import db_config
from datetime import datetime
import pandas as pd
from dateutil import parser

dash = Blueprint('dashboard', __name__,static_url_path='/static',static_folder='./static',template_folder="./templates")

@dash.route('/',methods= ["GET"])
@admin_required()
def home():
    counts = get_table_data_counts()
    print(counts)
    return render_template('index.html', counts = counts, admin_name=session.get("username"))


@dash.route('/UserList')
@admin_required()
def show_usersList():
    return render_template('user_list.html')

@dash.route('/ArtistList')
@admin_required()
def show_artistList():
    return render_template('artist_list.html')

@dash.route('/users_data', methods=['POST'])
@admin_required()
def user_data():
    columns = ['id', 'first_name', 'last_name', 'email','phone']

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

@dash.route('/artist_data', methods=['POST'])
@admin_required()
def artist_data():
    columns = ['id', 'name', 'dob','address', 'gender','first_release_year','no_of_albums_released','created_at']

    draw = request.form.get('draw')
    start = request.form.get('start')
    length = request.form.get('length')
    search_value = request.form.get('search[value]')

    with psycopg2.connect(db_config) as connection, connection.cursor() as cursor:
        base_query = f"SELECT {', '.join(columns)} FROM artist"

        if search_value:
            search_query = f"{base_query} WHERE name ILIKE '%{search_value}%'"
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

@dash.route('/view_albums/<id>', methods=['POST','GET'])
@admin_required()
def view_artist_albums(id):
    if request.method =='POST':
        columns = ['title', 'album_name','genre','created_at']

        draw = request.form.get('draw')
        start = request.form.get('start')
        length = request.form.get('length')
        search_value = request.form.get('search[value]')

        with psycopg2.connect(db_config) as connection, connection.cursor() as cursor:
            base_query = f"SELECT {', '.join(columns)} FROM music WHERE artist_id = {id}"

            if search_value:
                search_query = f"{base_query} AND title ILIKE '%{search_value}%'"
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
    return render_template('album_list.html', id= id)

@dash.route('/userdata/<id>', methods=['POST', 'GET'])
@admin_required()
def user_D(id):
	user = fetch_userId(id)
	print(user)
	return render_template('register_admin.html',submitted_data=user)
     

@dash.route('/register_user',methods= ['POST','GET'])
def register_user():
    if request.method =='POST':
        registeredUser_info ={
            "first_name": request.form.get('first_name'),
            "last_name" : request.form.get('last_name'),
            "email" : request.form.get('email'),
            "dob" : request.form.get('dob'),
            "phonenumber" : request.form.get('phonenumber'),
            "address" : request.form.get('address'),
            "gender" : request.form.get('gender'),
            "password" : request.form.get('password'),
            }
        dob = registeredUser_info.get('dob')
        session['submitted_data'] = request.form

        registeredUser_info['dob'] = datetime.fromisoformat(dob) if dob!= None else ""
        form = registerAdminForm(**registeredUser_info)
        form = form.validate()
        if form["success"]:
            session.pop('submitted_data', None)
            validate_user = user_registration(registeredUser_info)
            if validate_user["success"]:
                return redirect('/UserList')

            flash(validate_user["message"], 'danger')            
            return redirect('/UserList')
            
        flash(form["message"], 'danger')
        return redirect('/UserList')
        
    submitted_data = session.get('submitted_data', {})
    return render_template('register_user.html',submitted_data=submitted_data)

@dash.route('/edit_user/<id>',methods= ['POST','GET'])
def edit_user_route(id):
    if request.method =='POST':
        registeredUser_info ={
            "first_name": request.form.get('first_name'),
            "last_name" : request.form.get('last_name'),
            "email" : request.form.get('email'),
            "dob" : request.form.get('dob'),
            "phonenumber" : request.form.get('phonenumber'),
            "address" : request.form.get('address'),
            "gender" : request.form.get('gender'),
            "password" : request.form.get('password'),
            }
        dob = registeredUser_info.get('dob')
        session['submitted_data'] = request.form

        registeredUser_info['dob'] = datetime.fromisoformat(dob) if dob!= None else ""
        form = registerAdminForm(**registeredUser_info)
        form = form.validate()
        if form["success"]:
            session.pop('submitted_data', None)
            registeredUser_info['id']= id
            validate_user = edit_user(registeredUser_info)
            if validate_user["success"]:
                return redirect('/UserList')
            flash(validate_user["message"], 'danger')            
            return redirect('/UserList')
        flash(form["message"], 'danger')
        return redirect('/UserList')
    user = fetch_userId(id)
    return render_template('edit_user.html',submitted_data=user)

@dash.route('/delete_user/<id>',methods= ['POST','GET'])
def delete_user_route(id):  
    delete_user(id)
    return redirect('/UserList') 

@dash.route('/delete_artist/<id>',methods= ['POST','GET'])
def delete_artist_route(id):  
    delete_artist(id)
    return redirect('/ArtistList') 

@dash.route('/delete_artists_music/<id>/<title>',methods= ['POST','GET'])
def delete_artists_music(id,title):  
    delete_song(id,title)
    return redirect(f'/view_albums/{id}')
 

@dash.route('/edit_artist/<id>',methods= ['POST','GET'])
def edit_artist_route(id):
    if request.method =='POST':
        registeredArtist_info ={
            "name": request.form.get('name'),
            "dob" : request.form.get('dob'),
            "gender" : request.form.get('gender'),
            "address" : request.form.get('address'),
            "first_release_year" : request.form.get('first_release_year'),
            "no_of_albums_released" : request.form.get('no_of_albums_released'),
            }
        dob = registeredArtist_info.get('dob')
        noa = registeredArtist_info.get('no_of_albums_released')
        session['submitted_data'] = request.form

        registeredArtist_info['dob'] = datetime.fromisoformat(dob) if dob!= None else ""
        registeredArtist_info['no_of_albums_released'] = int(noa ) if dob!= None else 1
        form = registerArtistForm(**registeredArtist_info)
        form = form.validate()
        if form["success"]:
            session.pop('submitted_data', None)
            registeredArtist_info['id']= id
            validate_user = edit_artist(registeredArtist_info)
            if validate_user["success"]:
                return redirect('/ArtistList')
            flash(validate_user["message"], 'danger') 
            return redirect('/register_artist')           
        flash(form["message"], 'danger')
        return redirect('/register_artist')
    artist = fetch_artistId(id)
    return render_template('edit_artist.html',submitted_data=artist)

@dash.route('/register_artist',methods= ['POST','GET'])
def register_artist():
    if request.method =='POST':
        registeredArtist_info ={
            "name": request.form.get('name'),
            "dob" : request.form.get('dob'),
            "gender" : request.form.get('gender'),
            "address" : request.form.get('address'),
            "first_release_year" : request.form.get('first_release_year'),
            "no_of_albums_released" : request.form.get('no_of_albums_released'),
            }
        dob = registeredArtist_info.get('dob')
        noa = registeredArtist_info.get('no_of_albums_released')
        session['submitted_data'] = request.form

        registeredArtist_info['dob'] = datetime.fromisoformat(dob) if dob!= None else ""
        registeredArtist_info['no_of_albums_released'] = int(noa ) if noa!= None else 1
        form = registerArtistForm(**registeredArtist_info)
        form = form.validate()
        if form["success"]:
            session.pop('submitted_data', None)
            validate_user = artist_registration(registeredArtist_info)
            if validate_user["success"]:
                return redirect('/ArtistList')
            flash(validate_user["message"], 'danger') 
            return redirect('/register_artist')           
        flash(form["message"], 'danger')
        return redirect('/register_artist')
    submitted_data = session.get('submitted_data', {})
    return render_template('register_artist.html',submitted_data=submitted_data)


@dash.route('/register_music/<id>',methods= ['POST','GET'])
def register_music(id):
    if request.method =='POST':
        registeredMusic_info ={
            "title": request.form.get('title'),
            "album_name" : request.form.get('album_name'),
            "genre" : request.form.get('genre'),
            }
        session['submitted_data'] = request.form
        id = int(id) if id.isnumeric() else id

        form = registerMusicForm(**registeredMusic_info)
        form = form.validate()
        if form["success"]:
            session.pop('submitted_data', None)
            validate_user = music_registration(registeredMusic_info, id)
            if validate_user["success"]:
                return redirect(f'/view_albums/{id}')
            flash(validate_user["message"], 'danger') 
            return redirect(f'/view_albums/{id}')
         
        flash(form["message"], 'danger')
        return redirect(f'/view_albums/{id}')

    submitted_data = session.get('submitted_data', {})
    return render_template('register_music.html',submitted_data=submitted_data, id = id)


@dash.route('/edit_album/<id>/<title>',methods= ['POST','GET'])
def edit_music(id,title):
    song_details =fetch_artistsong(id,title)
    if request.method =='POST':
        registeredMusic_info ={
            "title": request.form.get('title'),
            "album_name" : request.form.get('album_name'),
            "genre" : request.form.get('genre'),
            }
        session['submitted_data'] = request.form
        id = int(id) if id.isnumeric() else id

        form = registerMusicForm(**registeredMusic_info)
        form = form.validate()
        if form["success"]:
            session.pop('submitted_data', None)
            registeredMusic_info['prev_title']=title
            validate_user = edit_Amusic(registeredMusic_info, id)
            if validate_user["success"]:
                return redirect(f'/view_albums/{id}')
            flash(validate_user["message"], 'danger') 
            return redirect(f'/view_albums/{id}')
         
        flash(form["message"], 'danger')
        return redirect(f'/view_albums/{id}')

    return render_template('edit_music.html',submitted_data=song_details, id = id,title=title)

@dash.route('/upload_csv', methods=['POST'])
def upload_csv():
    csv_file = request.files['csv_file']
    if csv_file and allowed_file(csv_file.filename):
        try:
            df = pd.read_csv(csv_file)
            
            with psycopg2.connect(db_config) as connection:
                with connection.cursor() as cursor:
                    table_name = "artist"
                    
                    for _, row in df.iterrows():
                        filtered_dict = {key: row[key] for key in ['name', 'dob', 'gender','address','first_release_year','no_of_albums_released']}
                        dob =filtered_dict.get('dob')
                        noa =filtered_dict.get('no_of_albums_released')
                        filtered_dict['dob'] = parser.parse(dob) if dob!= None else ""
                        filtered_dict['no_of_albums_released'] = int(noa ) if dob!= None else 1
                        form = registerArtistForm(**filtered_dict)
                        form = form.validate()
                        if form["success"]:
                            session.pop('submitted_data', None)
                            validate_user = artist_registration(filtered_dict)
                            if validate_user["success"]:
                                flash(f"{row['name']}'s document inserted.", 'success') 
                            else:
                                flash(f"{row['name']}'s document insertion failed. Reason: {validate_user['message']}", 'danger')

                        else:
                            flash(form["message"], 'danger')
            return redirect('/ArtistList')
            
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return redirect('/ArtistList')
    else:
        flash('Invalid file format. Please upload a CSV file.', 'danger')
    
    return redirect('/ArtistList')

