#!/bin/bach

# Créé l'environnement virtuel de python et installer les requirements
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt

# Crée le fichier .flaskenv
touch .flaskenv
echo "FLASK_APP = src" > .flaskenv
echo "FLASK_DEBUG = True" >> .flaskenv

# Load la base de donnée
cd src/
flask loaddb src/data.yml

