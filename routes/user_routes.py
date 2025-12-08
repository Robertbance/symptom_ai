
from flask import Blueprint, request, jsonify, render_template
from database.queries import (
    create_user,
    get_user_by_email,
    get_user_by_id,
    get_diagnostics_for_user
)
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import uuid


#  BLUEPRINT de l'utilisateur

user_bp = Blueprint("user", __name__)


def uuid4_hex():
    """Génère un id_user string unique."""
    return uuid.uuid4().hex


# ROUTES TEMPLATES HTML

@user_bp.route("/register", methods=["GET"])
def register_page():
    return render_template("register.html")


@user_bp.route("/login", methods=["GET"])
def login_page():
    return render_template("login.html")


@user_bp.route("/profile", methods=["GET"])
def profile_page():
    return render_template("profile.html")


@user_bp.route("/history", methods=["GET"])
def history_page():
    return render_template("history.html")


#  API : INSCRIPTION
@user_bp.route("/register", methods=["POST"])
def register_api():
    data = request.get_json(force=True)

    # Champs requis
    email = data.get("email_user", "").strip().lower()
    pwd = data.get("password", "")

    if not email or not pwd:
        return jsonify({"error": "Email et mot de passe requis"}), 400

    # Vérifier si email existe déjà
    if get_user_by_email(email):
        return jsonify({"error": "Email déjà utilisé"}), 400

    # Vérification âge
    try:
        age = int(data.get("age_user"))
    except Exception:
        return jsonify({"error": "age_user doit être un entier"}), 400

    # Construction utilisateur
    new_user = {
        "id_user": uuid4_hex(),
        "nom_user": data.get("nom_user", "").strip(),
        "prenom_user": data.get("prenom_user", "").strip(),
        "email_user": email,
        "sexe_user": data.get("sexe_user", "").strip(),
        "age_user": age,
        "date_inscrit_user": datetime.utcnow(),
        "password_hash": generate_password_hash(pwd),
        "is_admin": False,
    }

    create_user(new_user)

    return jsonify({
        "message": "Inscription réussie",
        "id_user": new_user["id_user"]
    }), 201


#  API : CONNEXION
@user_bp.route("/login", methods=["POST"])
def login_api():
    data = request.get_json(force=True)

    email = data.get("email_user", "").strip().lower()
    pwd = data.get("password", "")

    if not email or not pwd:
        return jsonify({"error": "Champs manquants"}), 400

    user = get_user_by_email(email)
    if not user:
        return jsonify({"error": "Email ou mot de passe incorrect,veuillez réesayer svp!!!"}), 401

    if not check_password_hash(user.get("password_hash", ""), pwd):
        return jsonify({"error": "Email ou mot de passe incorrect,veuillez réesayer svp!!!"}), 401

    return jsonify({
        "id_user": user.get("id_user"),
        "is_admin": user.get("is_admin", False)
    }), 200


#  API : PROFIL UTILISATEUR
@user_bp.route("/profile/data", methods=["POST"])
def profile_data():
    data = request.get_json(force=True)
    id_user = str(data.get("id_user", "")).strip()

    if not id_user:
        return jsonify({"error": "id_user requis"}), 400

    user = get_user_by_id(id_user)
    if not user:
        return jsonify({"error": "Utilisateur introuvable"}), 404

    # Supprimer le hash du mot de passe
    user.pop("password_hash", None)
    user.pop("_id", None)

    # Conversion de la date en string
    if "date_inscrit_user" in user and hasattr(user["date_inscrit_user"], "isoformat"):
        user["date_inscrit_user"] = user["date_inscrit_user"].isoformat()

    return jsonify(user), 200


#  API : HISTORIQUE DES DIAGNOSTICS

@user_bp.route("/history/data", methods=["POST"])
def history_data():
    data = request.get_json(force=True)
    id_user = str(data.get("id_user", "")).strip()

    if not id_user:
        return jsonify({"error": "id_user requis"}), 400

    diagnostics = list(get_diagnostics_for_user(id_user))

    # Nettoyage pour le frontend
    for d in diagnostics:
        d.pop("_id", None)
        if "date_diagnostic" in d and hasattr(d["date_diagnostic"], "isoformat"):
            d["date_diagnostic"] = d["date_diagnostic"].isoformat()

    return jsonify({"diagnostics": diagnostics}), 200
