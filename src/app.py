from flask import Flask
from flask_bootstrap import Bootstrap5
import os.path
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = "# TODO : Add your secret key"
app.config['BOOTSTRAP_SERVE_LOCAL'] = True
Bootstrap = Bootstrap5(app)

def mkpath(p):
    return os.path.normpath(
        os.path.join(
            os.path.dirname(__file__),
            p))

app.config["SQLALCHEMY_DATABASE_URI"] ="sqlite:///" + mkpath ("../myapp.db")

db = SQLAlchemy(app)