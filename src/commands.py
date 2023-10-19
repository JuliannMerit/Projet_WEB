import click
from .app import app, db

@app.cli.command()
@click.argument('filename')
def loaddb(filename):
    "Creates the tables and populates them with data. "
    # suppression de toutes les tables
    db.drop_all()
    # création de toutes les tables
    db.create_all()
    # chargement de notre jeu de données
    import yaml
    films = yaml.safe_load(open(filename))
    # import des modèles
    from .models import Realisateur, Film
    # première passe: création de tous les réalisateurs
    realisateur = {}
    for f in films:
        r = f['realisateur']
        if r not in realisateur:
            o = Realisateur(nom=r)
            db.session.add(o)
            realisateur[r] = o
    db.session.commit()
    # deuxième passe: création de tous les films
    for f in films:
        r = realisateur[f["realisateur"]]
        print(r)
        o = Film(nom_film = f["nom_film"],
                genre = f["genre"],
                img = f["img"],
                lien = f["lien"],
                id_realisateur = r.id)
        db.session.add(o)
    db.session.commit()

@app.cli.command()
def syncdb():
    "Creates all missing tables. "
    db.create_all()

@app.cli.command()
@click.argument('username')
@click.argument('password')
def newuser(username,password):
    "Creates a new user. "
    from .models import User
    from hashlib import sha256
    m=sha256()
    m.update(password.encode())
    u=User(username=username,password=m.hexdigest())
    db.session.add(u)
    db.session.commit()
    
@app.cli.command()
@click.argument('username')
@click.argument('newpassword')
def passwd(username,newpassword):
    "Changes the password of a user. "
    from .models import User
    from hashlib import sha256
    m=sha256()
    m.update(newpassword.encode())
    u=User.query.get(username)
    u.password=m.hexdigest()
    db.session.commit()