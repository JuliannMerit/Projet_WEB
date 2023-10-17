import click
from .app import app, db


# import des modèles
from . models import Realisateur, Film


@app.cli.command()
@click.argument('filename')
def loaddb(filename):
    "Creates the tables and populates them with data. "
    # création de toutes les tables
    db.create_all()
    # chargement de notre jeu de données
    import yaml
    films = yaml.safe_load(open(filename))
    # première passe: création de tous les réalisateurs
    realisateur = {}
    for f in films:
        r = f["author"]
        if r not in realisateur:
            o = Realisateur(name=r)
            db.session.add(o)
            realisateur[r] = o
    db.session.commit()
    # deuxième passe: création de tous les films
    for f in films:
        a = realisateur[f["realisateur"]]
        o = Film(
            nom = f["nom_film"],
            genre = f["genre"],
            img = f["img"],
            url = f["url"],
            realisateur = a)
        db.session.add(o)
    db.session.commit()
