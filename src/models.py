import yaml, os.path
from .app import db, login_manager
from flask_login import UserMixin

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

class Realisateur(db.Model):
    """Class représentant un réalisateur de film

    Args:
        db (SQLAlchemy): Base de données
    
    Attributes:
        id (int): Identifiant unique du réalisateur
        nom (str): Nom du réalisateur
    """
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(64), nullable=False)
    
    
    def __repr__(self):
        """Méthode d'affichage de la classe Realisateur

        Returns:
            str: Nom du réalisateur
        """
        return self.nom

class Film(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom_film = db.Column(db.String(64), nullable=False)
    genre = db.Column(db.String(64), nullable=False)
    img = db.Column(db.String(200), nullable=False)
    lien = db.Column(db.String(250), nullable=False)
    id_realisateur = db.Column(db.Integer, db.ForeignKey('realisateur.id'), nullable=False)
    realisateur = db.relationship('Realisateur', backref=db.backref('films', lazy='dynamic'))
    
    def __repr__(self):
        return self.nom_film

class User(db.Model, UserMixin):
    username = db.Column(db.String(64), primary_key=True)
    password = db.Column(db.String(64))
    
    def get_id(self):
        return self.username

class Commentaire(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    commentaire = db.Column(db.String(500), nullable=False)
    id_film = db.Column(db.Integer, db.ForeignKey('film.id'), nullable=False)
    nom_user = db.Column(db.String(64), db.ForeignKey('user.username'), nullable=False)
    film = db.relationship('Film', backref=db.backref('commentaires', lazy='dynamic'))

    def __repr__(self):
        return self.commentaire

def get_sample():
    return Film.query.all()

def get_realisateur(id):
    return Realisateur.query.get(id)

def get_commentaires(id):
    return Commentaire.query.filter_by(id_film=id).all()

@login_manager.user_loader
def load_user(username):
    return User.query.get(username)