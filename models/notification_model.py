# models/notification_model.py
"""
Schéma et helpers pour la collection 'notification'.
"""

from datetime import datetime
from typing import Dict, Any

REQUIRED_FIELDS = ["id_notification", "message_notification", "id_user"]


def build_notification_document(data: Dict[str, Any]) -> Dict[str, Any]:
    missing = [f for f in REQUIRED_FIELDS if f not in data]
    if missing:
        raise ValueError(f"Champs obligatoires manquants: {missing}")

    return {
        "id_notification": data["id_notification"],
        "message_notification": data.get("message_notification", "").strip(),
        "date_notification": data.get("date_notification", datetime.utcnow()),
        "statut_notification": data.get("statut_notification", "").strip(),
        "id_user": data["id_user"]
    }
