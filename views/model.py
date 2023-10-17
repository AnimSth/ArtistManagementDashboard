# from extensions import db
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email
from werkzeug.security import generate_password_hash, check_password_hash
from email_validator import validate_email, EmailNotValidError
from phonenumbers import geocoder
import phonenumbers, uuid
# from sqlalchemy.dialects.postgresql import UUID 

# class User(db.Model):
#     __tablename__ = 'users'
#     id = db.Column(db.Integer, primary_key=True)
#     first_name = db.Column(db.String(255), nullable=False)
#     last_name = db.Column(db.String(255), nullable=False)
#     email = db.Column(db.String(255), unique=True, nullable=False)
#     password = db.Column(db.String(500), nullable=False)
#     phone = db.Column(db.String(20))
#     dob = db.Column(db.Date)
#     gender = db.Column(db.String(10))
#     address = db.Column(db.String(255))
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)
#     updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

#     def __init__(self, first_name, last_name, email, password, phone, dob, gender, address):
#         self.first_name = first_name
#         self.last_name = last_name
#         self.email = email
#         self.password = password
#         self.phone = phone
#         self.dob = dob
#         self.gender = gender
#         self.address = address

#     def __repr__(self):
#         return f"<User {self.first_name} {self.last_name}>"

# class BlackList(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(255), unique=True, nullable=False)

#     def __init__(self, email):
#         self.email = email

#     def __repr__(self):
#         return f"<User {self.first_name} {self.last_name}>"


class LoginForm():
    def __init__(self, email, password):
        self.email = email
        self.password= password

    def validate(self):
        try:
            validate_email(self.email)
            if not isinstance(self.email, str):
                return {"success":False,"message":"Please enter a valid email."}        
            return {"success":True,"message":"Please proceed."}
        except:
            return {"success":False,"message":"Please enter a valid email."}      

class registerAdminForm():
    def __init__(self,first_name,last_name, phonenumber,address,dob,gender,email, password):
        self.first_name :str = first_name
        self.last_name:str= last_name
        self.email:str = email
        self.phonenumber: int= phonenumber
        self.address: str = address
        self.dob: datetime= dob
        self.gender: str = gender
        self.password: str= password

    def validate(self):
        try:
            validate_email(self.email)
            if not isinstance(self.email, str):
                return {"success":False,"message":"Please enter a valid email."}   
            if not isinstance(self.dob, datetime):
                return {"success":False,"message":"Please enter a valid date of birth."}    
             
            if len(str(self.phonenumber))!= 10 or check_number(self.phonenumber):
                return {"success":False,"message":"Please enter a valid number.",}

            if self.gender not in ['f',"m",'o']:
                return {"success":False,"message":"Please choose a gender."}
            
            if len(self.first_name or self.last_name) < 2 or len(self.first_name or self.last_name) > 255:
                return {"success":False,"message":"Name must be between 2 and 255 characters."}
            
            if len(self.last_name) < 2 or len(self.last_name) > 255:
                return {"success": False, "message": "Last name must be between 2 and 255 characters."}

            if not self.first_name.isalpha() and not self.first_name.isspace() or not self.last_name.isalpha() and not self.last_name.isspace():
                return {"success":False,"message":"Name must be between 2 and 100 characters."}
            
            return {"success":True, "message":"Please proceed."}
        except:
            return {"success":False,"message":"Please enter a valid email."}    

def check_number(number):
    ch_number = phonenumbers.parse(f"+977{number}","CH")
    country = geocoder.description_for_number(ch_number,"en")
    if country != 'Nepal':
        return True 
    return False

class registerArtistForm():
    def __init__(self,name,address,dob,gender,first_release_year, no_of_albums_released):
        self.name :str = name
        self.address: str = address
        self.dob: datetime= dob
        self.gender: str = gender
        self.first_release_year: datetime = first_release_year
        self.no_of_albums_released: int = no_of_albums_released


    def validate(self):
        if not isinstance(self.dob, datetime) and not isinstance(self.first_release_year, datetime):
            return {"success":False,"message":"Please enter a valid date."}    
            
        if not isinstance(self.no_of_albums_released, int):
            return {"success":False,"message":"Please enter a valid no. of albums released."}    

        if self.gender not in ['f',"m",'o']:
            return {"success":False,"message":"Please choose a gender."}
        
        if len(self.name) < 2 or len(self.name) > 255:
            return {"success":False,"message":"Name must be between 2 and 255 characters."}

        if not self.name.replace(' ','').isalpha():
            return {"success":False,"message":"Name must be between 2 and 100 characters."}
        
        return {"success":True, "message":"Please proceed."}

