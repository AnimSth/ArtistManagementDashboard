from flask import Flask, render_template, request, redirect, url_for
from flask_wtf.csrf import CSRFProtect
from db import init_db
import os
# from dotenv import load

app = Flask(__name__)
app.config['SECRET_KEY'] = "weDontTHings,thIngsOwnus"
csrf = CSRFProtect(app)

from views.authentication.auth import authenticate
from views.dashboard.home import dash

app.register_blueprint(authenticate)
app.register_blueprint(dash)


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
