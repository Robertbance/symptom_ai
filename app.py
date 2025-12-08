import sys
import os
import json
from datetime import datetime

from flask import Flask, render_template, jsonify
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler
from pywebpush import webpush

#  Connexion MongoDB
from database.mongo_connection import db

# --- Chemin racine -
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

# --- Import blueprints ---
from routes.user_routes import user_bp
from routes.chatbot_routes import chatbot_bp
from routes.diagnostic_routes import diagnostic_bp
from routes.maladie_routes import maladie_bp


# --- Flask App ---
app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static")
)

CORS(app)


# -------------------------------------------------------------------
#  Fonction d'envoi des notifications programmées
# -------------------------------------------------------------------
def send_reminder_notifications():
    now = datetime.utcnow()

    users = db.users.find({
        "last_diagnostic": {"$exists": True},
        "notifications_sent": {"$lt": 6}
    })

    for user in users:
        subscription = user.get("push_subscription")
        last_diag = user["last_diagnostic"]
        sent = user.get("notifications_sent", 0)

        delta = now - last_diag
        hours = delta.total_seconds() / 3600

        # Test rapide : 0.01h = 36 secondes
        if hours >= (sent + 1) * 0.01 and delta.days < 3:

            if subscription:
                data = {
                    "title": "Rappel SymptomAI",
                    "message": "Pensez à vérifier l'évolution de vos symptômes."
                }

                try:
                    webpush(
                        subscription_info=subscription,
                        data=json.dumps(data),
                        vapid_private_key=os.getenv("VAPID_PRIVATE_KEY"),
                        vapid_claims={"sub": "mailto:contact@symptomai.com"}
                    )

                    # Mise à jour compteur notifications
                    db.users.update_one(
                        {"_id": user["_id"]},
                        {"$inc": {"notifications_sent": 1}}
                    )

                except Exception as e:
                    print("Erreur lors de l'envoi d'une notification :", e)


# -------------------------------------------------------------------
#  Scheduler (TEST → chaque minute)
# -------------------------------------------------------------------
scheduler = BackgroundScheduler()
scheduler.add_job(send_reminder_notifications, "interval", minutes=1)
scheduler.start()


# -------------------------------------------------------------------
#  ROUTES FRONTEND
# -------------------------------------------------------------------
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


# -------------------------------------------------------------------
#  ROUTES API
# -------------------------------------------------------------------
app.register_blueprint(user_bp, url_prefix="/user")
app.register_blueprint(chatbot_bp, url_prefix="/chatbot")
app.register_blueprint(diagnostic_bp, url_prefix="/diagnostic")
app.register_blueprint(maladie_bp, url_prefix="/maladie")


# -------------------------------------------------------------------
#  GESTION DES ERREURS
# -------------------------------------------------------------------
@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Route introuvable"}), 404


@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Erreur interne du serveur"}), 500


# -------------------------------------------------------------------
#  LANCEMENT SERVEUR
# -------------------------------------------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

