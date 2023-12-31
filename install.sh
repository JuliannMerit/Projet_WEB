#!/bin/bach

# Créé l'environnement virtuel de python et installer les requirements
set -e
virtualenv -p python3 venv
source "./venv/bin/activate"
pip install -r requirements.txt
pip install Werkzeug==2.3.7

# Crée le fichier .flaskenv
touch .flaskenv
echo "FLASK_APP = src" > .flaskenv
echo "FLASK_DEBUG = True" >> .flaskenv

# Load la base de donnée
flask loaddb src/data.yml

deactivate
