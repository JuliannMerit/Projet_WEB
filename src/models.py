import yaml, os.path
from .app import db#, login_manager
#from flask_login import UserMixin

Films = yaml.safe_load(
    open(
        os.path.join(
            os.path.dirname(__file__),
            'data.yml'
        )
    )
)

i = 0
for film in Films:
    film['id'] = i
    i += 1

def get_sample():
    return Films[1:10]

class Realisateur(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(64), nullable=False)
    prenom = db.Column(db.String(64), nullable=False)
    
    def __repr__(self):
        return self.nom + self.prenom

#Realisateur, nom_film, genre, lien, image, id
class Film(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom_film = db.Column(db.String(64), nullable=False)
    genre = db.Column(db.String(64), nullable=False)
    img = db.Column(db.String(200), nullable=False)
    url = db.Column(db.String(250), nullable=False)
    id_realisateur = db.Column(db.Integer, db.ForeignKey('realisateur.id'), nullable=False)
    realisateur = db.relationship('realisateur', backref=db.backref('films', lazy='dynamic'))
    
    def __repr__(self):
        return self.nom_film


def get_sample2():
    return Film.query.limit(10).all()

def get_realisateur():
    return Realisateur.query.all()

#class User(db.Model, UserMixin):
#    username = db.Column(db.String(64), primary_key=True)
#    password = db.Column(db.String(64), nullable=False)
#    
#    def get_id(self):
#        return self.username

#@login_manager.user_loader
#def load_user(username):
#    return User.query.get(username)