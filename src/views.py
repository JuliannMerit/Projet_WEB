from .app import app
from flask import render_template, url_for
from .models import get_sample
#from .commands import*
#from .views import *
from flask_wtf import FlaskForm
from wtforms import StringField , HiddenField, PasswordField
from wtforms.validators import DataRequired
from hashlib import sha256

class AuthorForm(FlaskForm):
    id = HiddenField('id')
    name = StringField('Nom', validators =[ DataRequired ()])

@app.route('/')
def home():
    return render_template('home.html',
                           title="Hello World",
                           books=get_sample())