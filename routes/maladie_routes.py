# routes/maladie_routes.py

from flask import Blueprint, request, jsonify
from database.queries import (
    create_maladie,
    get_maladie_by_id,
    get_all_maladies
)
from models.maladie_model import build_maladie_document

maladie_bp = Blueprint("maladie", __name__)


# Obtenir la Liste de toutes les maladies

@maladie_bp.route("/all", methods=["GET"])
def list_maladies():
    try:
        maladies = get_all_maladies()

        # Nettoyage MongoDB
        for m in maladies:
            m.pop("_id", None)

        return jsonify({
            "count": len(maladies),
            "maladies": maladies
        }), 200

    except Exception as e:
        return jsonify({
            "error": "Erreur serveur lors du chargement des maladies",
            "detail": str(e)
        }), 500


#  GET : Récupérer une maladie par ID

@maladie_bp.route("/<id_maladie>", methods=["GET"])
def maladie_detail(id_maladie):
    try:
        maladie = get_maladie_by_id(id_maladie)

        if not maladie:
            return jsonify({"error": "Maladie introuvable"}), 404

        maladie.pop("_id", None)

        return jsonify(maladie), 200

    except Exception as e:
        return jsonify({
            "error": "Erreur serveur lors de la récupération de la maladie",
            "detail": str(e)
        }), 500


#  POST : Ajouter une nouvelle maladie
@maladie_bp.route("/add", methods=["POST"])
def add_maladie():
    try:
        data = request.get_json(force=True)

        # Construction et validation du document
        doc = build_maladie_document(data)

        inserted_id = create_maladie(doc)

        return jsonify({
            "message": "Maladie ajoutée avec succès",
            "id": str(inserted_id)
        }), 201

    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    except Exception as e:
        return jsonify({
            "error": "Erreur serveur lors de l'ajout de la maladie",
            "detail": str(e)
        }), 500
