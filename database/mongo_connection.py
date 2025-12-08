from pymongo import MongoClient
import config
#Connexion de la base de données
def get_database():

    client = MongoClient(config.MONGO_URI)
    db = client[config.DB_NAME]
    return db

# Base de données utilisée dans tout le projet
db = get_database()

# Les collections de ma base de données 'chat_intelligent'
users_col = db["utilisateur"]
maladies_col = db["maladie"]
symptomes_col = db["symptome"]
diagnostics_col = db["diagnostic"]
notifications_col = db["notification"]

def get_db():
    """Retourne l’objet base de données MongoDB."""
    return db
