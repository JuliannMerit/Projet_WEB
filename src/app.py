from flask import Flask
from flask_bootstrap import Bootstrap5
import os.path
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = "3955c6ec-db88-4723-804a-0e46f26f198b"
app.config['BOOTSTRAP_SERVE_LOCAL'] = True
Bootstrap = Bootstrap5(app)

def mkpath(p):
    return os.path.normpath(
        os.path.join(
            os.path.dirname(__file__),
            p))

app.config["SQLALCHEMY_DATABASE_URI"] ="sqlite:///" + mkpath("../myapp.db")
db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login' # Change this to the name of your login view function