from flask import (Blueprint, 
	render_template, 
	request, url_for, 
	redirect,session,
	flash,
	jsonify,
	Response)
import json
# from extensions import db
from datetime import datetime
from .controller import *
from ..model import LoginForm,registerAdminForm

authenticate = Blueprint('authentication', __name__,static_url_path='/static',static_folder='./static',template_folder="./templates")


@authenticate.route('/login',methods= ['POST','GET'])
@logged_in
def login():
    if request.method =='POST':
        login_info ={
            "email": request.form.get('email'),
            "password" : request.form.get('password')
            }
        form = LoginForm(**login_info)
        form = form.validate()

        if form["success"]:
            validate_user = user_validation(login_info)

            if validate_user["success"]:
                return redirect('/')
            flash(validate_user['message'],"danger")
            return redirect('/login')
        
        flash(form["message"], 'danger')
        return redirect('/login')

    return render_template('login.html')

@authenticate.route('/register_admin',methods= ['POST','GET'])
def register_admin():
    if request.method =='POST':
        registeredAdmin_info ={
            "first_name": request.form.get('first_name'),
            "last_name" : request.form.get('last_name'),
            "email" : request.form.get('email'),
            "dob" : request.form.get('dob'),
            "phonenumber" : request.form.get('phonenumber'),
            "address" : request.form.get('address'),
            "gender" : request.form.get('gender'),
            "password" : request.form.get('password'),
            }
        dob = registeredAdmin_info.get('dob')
        session['submitted_data'] = request.form

        registeredAdmin_info['dob'] = datetime.fromisoformat(dob) if dob!= None else ""
        form = registerAdminForm(**registeredAdmin_info)
        form = form.validate()
        if form["success"]:
            session.pop('submitted_data', None)
            validate_user = admin_registration(registeredAdmin_info)
            if validate_user["success"]:
                return redirect('/login')
            flash(validate_user["message"], 'danger')            
            return redirect(url_for('authentication.register_admin'))
        flash(form["message"], 'danger')
        return redirect(url_for('authentication.register_admin'))
    submitted_data = session.get('submitted_data', {})
    return render_template('register_admin.html',submitted_data=submitted_data)

@authenticate.route('/logout',methods= ['POST','GET'])
def logout():
    session.clear()
    flash("You have been logged out!", "success")
    return redirect('/login')



    