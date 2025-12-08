"""
Schéma et helpers pour la collection 'notification'.
"""

from typing import Dict, Any
from datetime import datetime

REQUIRED_FIELDS = ["id_notification", "id_user", "contenu_notification"]


def build_notification_document(data: Dict[str, Any]) -> Dict[str, Any]:
    missing = [f for f in REQUIRED_FIELDS if f not in data]
    if missing:
        raise ValueError(f"Champs obligatoires manquants : {missing}")

    return {
        "id_notification": data["id_notification"],
        "id_user": data["id_user"],
        "contenu_notification": data.get("contenu_notification", "").strip(),
        "type_notification": data.get("type_notification", "general"),  # ex. RDV, traitement, info
        "date_creation": data.get("date_creation", datetime.utcnow()),
        "date_rappel": data.get("date_rappel"),  # optionnel
        "lu": data.get("lu", False)  # permet "marquer comme lu"
    }
