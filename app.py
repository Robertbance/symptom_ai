import sys
import os

from flask import Flask, render_template, jsonify

# Connexion MongoDB
from database.mongo_connection import db

# --------------------------------------------------
# Chemin racine
# --------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

# --------------------------------------------------
# Importation des blueprints
# --------------------------------------------------
from routes.user_routes import user_bp
from routes.chatbot_routes import chatbot_bp
from routes.diagnostic_routes import diagnostic_bp
from routes.maladie_routes import maladie_bp

# --------------------------------------------------
# Initialisation de l'application Flask
# --------------------------------------------------
app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static")
)

# --------------------------------------------------
# Routes frontend
# --------------------------------------------------
@app.route("/")
def index_page():
    return render_template("index.html")

@app.route("/login")
def login_page():
    return render_template("login.html")

@app.route("/register")
def register_page():
    return render_template("register.html")

@app.route("/chat")
def chat_page():
    return render_template("chat.html")

# --------------------------------------------------
# Routes API
# --------------------------------------------------
app.register_blueprint(user_bp, url_prefix="/user")
app.register_blueprint(chatbot_bp, url_prefix="/chatbot")
app.register_blueprint(diagnostic_bp, url_prefix="/diagnostic")
app.register_blueprint(maladie_bp, url_prefix="/maladie")

# --------------------------------------------------
# Gestion globale des erreurs
# --------------------------------------------------
@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Route introuvable"}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Erreur interne du serveur"}), 500

# --------------------------------------------------
# Lancement du serveur
# --------------------------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)
