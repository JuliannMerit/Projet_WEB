from .app import app
from flask import render_template, url_for, redirect
from .models import db, get_realisateur, User, get_sample, get_commentaires, Commentaire
from flask_wtf import FlaskForm
from wtforms import StringField , HiddenField, PasswordField, TextAreaField
from wtforms.validators import DataRequired
from hashlib import sha256
from flask_login import login_user, logout_user, login_required, current_user
from flask import request
from datetime import date

class RealisateurForm(FlaskForm):
    id = HiddenField('id')
    nom = StringField('Nom', validators =[ DataRequired ()])

class LoginForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')
    next = HiddenField()

    def get_authenticated_user(self):
        user = User.query.get(self.username.data)
        if user is None:
            return None
        m = sha256()
        m.update(self.password.data.encode())
        passwd = m.hexdigest()
        if passwd == user.password:
            return user
        else:
            return None

class RegisterForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')

    def create_user(self):
        user = User.query.get(self.username.data)
        if user is None:
            m = sha256()
            m.update(self.password.data.encode())
            passwd = m.hexdigest()
            user = User(username=self.username.data, password=passwd)
            db.session.add(user)
            db.session.commit()
            return user
        else:
            return None

class CommentaireForm(FlaskForm):
    commentaire = TextAreaField('Commentaire')
    id_film = HiddenField('id_film')
    
    def create_commentaire(self):
        commentaire = Commentaire.query.get(self.commentaire.data)
        if commentaire is None:
            nom_user = current_user.username
            date_commmentaire = date.today()
            commentaire = Commentaire(commentaire=self.commentaire.data,
                                      id_film=self.id_film.data, 
                                      nom_user=nom_user,
                                      date=date_commmentaire)
            db.session.add(commentaire)
            db.session.commit()
            return commentaire
        else:
            return None

@app.route('/')
def home():
    return render_template('home.html',
                           title="Voici la liste des films",
                           films=get_sample())
    
@app.route('/detail/<id>', methods=("GET", "POST"))
@login_required
def detail(id):
    films = get_sample()
    film = films[int(id)-1]
    nb_films = len(films)
    commentaires = get_commentaires(id)
    user = current_user.username
    f = CommentaireForm(id_film = int(id))
    today = date.today()
    if f.validate_on_submit():
        if f.commentaire.data != "":
            f.create_commentaire()
            return redirect(url_for('detail',
                                    nb_films=nb_films,
                                    id=f.id_film.data,
                                    user=user,
                                    today=today))
        else:
            return render_template('detail.html',
                                    film=film,
                                    commentaires=commentaires,
                                    form=f,
                                    user=user,
                                    today=today,
                                    nb_films=nb_films)
    return render_template('detail.html',
                            film=film,
                            commentaires=commentaires,
                            form=f,
                            user=user,
                            today=today,
                            nb_films=nb_films)

@app.route('/edit/realisateur/<id>')
@login_required
def edit_realisateur(id):
    r = get_realisateur(id)
    f = RealisateurForm(id = r.id, nom = r.nom)
    return render_template('edit_realisateur.html',
                            realisateur=r,
                            form=f)

@app.route('/save/realisateur/', methods=("POST",))
def save_realisateur():
    a = None
    f = RealisateurForm()
    if f.validate_on_submit():
        id = int(f.id.data)
        r = get_realisateur(id)
        r.nom = f.nom.data
        db.session.commit()
        return redirect(url_for('detail', id=r.id))
    r = get_realisateur(int(f.id.data))
    return render_template('edit_realisateur.html',
                            realisateur=r,
                            form=f)

@app.route('/login/',methods=("GET","POST"))
def login():
    f=LoginForm()
    if not f.is_submitted():
        f.next.data=request.args.get("next")
    if f.validate_on_submit():
        user=f.get_authenticated_user()
        if user:
            login_user(user)
            next=f.next.data or url_for("home")
            return redirect(next)
        else:
            return render_template("login.html",form=f)
    return render_template("login.html",form=f)

@app.route("/logout/")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/register/',methods=("GET","POST"))
def register():
    f=RegisterForm()
    if not f.is_submitted():
        return render_template("register.html",form=f)
    if f.validate_on_submit():
        user=f.create_user()
        if user:
            login_user(user)
            return redirect("/")
        else:
            return render_template("register.html",form=f)
    return render_template("register.html",form=f)