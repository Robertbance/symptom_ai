# Importation des collections de la base de données

from database.mongo_connection import (
    users_col,
    maladies_col,
    symptomes_col,
    diagnostics_col,
    notifications_col,
    db
)
from datetime import datetime


# Utilisateurs

def create_user(data: dict):

    """Ajoute un utilisateur dans la collection."""

    if "id_user" in data:
        data["id_user"] = str(data["id_user"])
    return users_col.insert_one(data).inserted_id


def get_user_by_email(email: str):
    """Retourne un utilisateur par email."""
    return users_col.find_one({"email_user": email})


def get_user_by_id(id_user: str):
    """
    Récupère un utilisateur par ID.
    """
    return users_col.find_one({"id_user": str(id_user)})


def update_user(id_user: str, update_data: dict):
    """Met à jour un utilisateur."""
    return users_col.update_one(
        {"id_user": str(id_user)},
        {"$set": update_data}
    )


def delete_user(id_user: str):
    """Supprime un utilisateur."""
    return users_col.delete_one({"id_user": str(id_user)})


#  MALADIES

def create_maladie(data: dict):
    """Ajoute une maladie."""
    if "id_maladie" in data:
        data["id_maladie"] = str(data["id_maladie"])
    return maladies_col.insert_one(data).inserted_id


def get_maladie_by_id(id_maladie: str):
    """Retourne une maladie."""
    return maladies_col.find_one({"id_maladie": str(id_maladie)})


def get_all_maladies():
    """Liste toutes les maladies."""
    return list(maladies_col.find({}))


#  SYMPTÔMES

def create_symptome(data: dict):
    """Ajoute un symptôme."""
    if "id_symptome" in data:
        data["id_symptome"] = str(data["id_symptome"])
    return symptomes_col.insert_one(data).inserted_id


def get_symptome_by_id(id_symptome: str):
    """Retourne un symptôme."""
    return symptomes_col.find_one({"id_symptome": str(id_symptome)})


def get_all_symptomes():
    """Liste tous les symptômes."""
    return list(symptomes_col.find({}))

# DIAGNOSTICS

def create_diagnostic(data: dict):
    """    Insère un diagnostic.
    """
    # Normalisation des IDs
    if "id_diagnostic" in data:
        data["id_diagnostic"] = str(data["id_diagnostic"])

    if "id_maladie" in data and data["id_maladie"] is not None:
        data["id_maladie"] = str(data["id_maladie"])

    if "id_user" in data and data["id_user"] is not None:
        data["id_user"] = str(data["id_user"])

    # Date automatique
    if "date_diagnostic" not in data:
        data["date_diagnostic"] = datetime.utcnow()

    # Définissons une structure symptômes
    if "symptomes" in data and isinstance(data["symptomes"], list):
        for s in data["symptomes"]:
            if "nom_symptome" in s and isinstance(s["nom_symptome"], str):
                continue  # valid
            else:
                s["nom_symptome"] = str(s.get("nom_symptome", ""))

    return diagnostics_col.insert_one(data).inserted_id


def get_diagnostic_by_id(id_diagnostic: str):
    """Retourne un diagnostic."""
    return diagnostics_col.find_one({"id_diagnostic": str(id_diagnostic)})


def get_diagnostics_for_user(id_user: str):
    """Liste tous les diagnostics d’un utilisateur."""
    return list(diagnostics_col.find({"id_user": str(id_user)}))


def delete_diagnostic(id_diagnostic: str):
    """Supprime un diagnostic."""
    return diagnostics_col.delete_one({"id_diagnostic": str(id_diagnostic)})


#  NOTIFICATIONS

def create_notification(data: dict):
    """Ajoute une notification."""
    if "id_notification" in data:
        data["id_notification"] = str(data["id_notification"])
    return notifications_col.insert_one(data).inserted_id


def get_notifications_for_user(id_user: str):
    """Liste les notifications d’un utilisateur."""
    return list(notifications_col.find({"id_user": str(id_user)}))


def update_notification_status(id_notification: str, new_status: str):
    """Met à jour le statut d'une notification."""
    return notifications_col.update_one(
        {"id_notification": str(id_notification)},
        {"$set": {"statut_notification": new_status}}
    )


#  OUTILS

def count_documents(collection_name: str):
    """Compte le nombre de documents dans une collection."""
    return db[collection_name].count_documents({})
