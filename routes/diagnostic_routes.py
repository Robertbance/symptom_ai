# routes/diagnostic_routes.py

from flask import Blueprint, request, jsonify
from datetime import datetime

from database.queries import (
    create_diagnostic,
    get_diagnostic_by_id,
    get_diagnostics_for_user,
    delete_diagnostic,
)
from database.mongo_connection import db
from models.diagnostic_model import build_diagnostic_document

diagnostic_bp = Blueprint("diagnostic", __name__)


# Sauvegarde d'un diagnostic
@diagnostic_bp.route("/save", methods=["POST"])
def save_diagnostic():
    """Enregistre un diagnostic complet envoyé par le frontend."""
    payload = request.get_json(force=True)

    try:
        # Construction du document diagnostic
        doc = build_diagnostic_document(payload)

        inserted_id = create_diagnostic(doc)

        # Mise à jour de la date du dernier diagnostic et remise à zéro du compteur
        user_id = payload.get("id_user")
        if user_id:
            db.users.update_one(
                {"_id": user_id},
                {
                    "$set": {
                        "last_diagnostic": datetime.utcnow(),
                        "notifications_sent": 0
                    }
                }
            )

        return jsonify({
            "message": "Diagnostic enregistré",
            "inserted_id": str(inserted_id)
        }), 201

    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    except Exception as e:
        return jsonify({
            "error": "Erreur serveur",
            "detail": str(e)
        }), 500


# Diagnostics par utilisateur
@diagnostic_bp.route("/user/<id_user>", methods=["GET"])
def list_user_diagnostics(id_user):
    """Renvoie la liste des diagnostics pour un utilisateur donné."""
    try:
        diags = get_diagnostics_for_user(id_user)

        nettoyer = []
        for d in diags:
            d.pop("_id", None)
            if "date_diagnostic" in d and hasattr(d["date_diagnostic"], "isoformat"):
                d["date_diagnostic"] = d["date_diagnostic"].isoformat()
            nettoyer.append(d)

        return jsonify({"diagnostics": nettoyer}), 200

    except Exception as e:
        return jsonify({
            "error": "Erreur serveur",
            "detail": str(e)
        }), 500


# Récupération d'un diagnostic par ID
@diagnostic_bp.route("/<id_diagnostic>", methods=["GET"])
def get_diagnostic(id_diagnostic):
    try:
        diag = get_diagnostic_by_id(id_diagnostic)

        if not diag:
            return jsonify({"error": "Diagnostic non trouvé"}), 404

        diag.pop("_id", None)

        if "date_diagnostic" in diag and hasattr(diag["date_diagnostic"], "isoformat"):
            diag["date_diagnostic"] = diag["date_diagnostic"].isoformat()

        return jsonify(diag), 200

    except Exception as e:
        return jsonify({
            "error": "Erreur serveur",
            "detail": str(e)
        }), 500


# Suppression d’un diagnostic
@diagnostic_bp.route("/<id_diagnostic>", methods=["DELETE"])
def remove_diagnostic(id_diagnostic):
    try:
        result = delete_diagnostic(id_diagnostic)

        if result.deleted_count == 0:
            return jsonify({"error": "Diagnostic non trouvé"}), 404

        return jsonify({"message": "Diagnostic supprimé"}), 200

    except Exception as e:
        return jsonify({
            "error": "Erreur serveur",
            "detail": str(e)
        }), 500
