#!/bin/bach

# Créé l'environnement virtuel de python et installer les requirements
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt

# Load la base de donnée
flask loaddb src/data.yml

# Crée le fichier .flaskenv
touch .flaskenv
echo "FLASK_APP = src" > .flaskenv
echo "FLASK_DEBUG = True" > .flaskenv