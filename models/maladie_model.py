"""
Schéma et helpers pour la collection 'maladie'.
"""

from typing import Dict, Any

# Champs obligatoires pour la création d'une maladie
REQUIRED_FIELDS = ["id_maladie", "nom_maladie"]


def build_maladie_document(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Construit et normalise un document 'maladie'.

    - Vérifie les champs obligatoires
    - Nettoie les chaînes (strip)
    - Accepte des champs additionnels sans casser
    """

    # Vérification des champs obligatoires
    missing = [f for f in REQUIRED_FIELDS if f not in data]
    if missing:
        raise ValueError(f"Champs obligatoires manquants: {missing}")

    # Document de base normalisé
    doc = {
        "id_maladie": data["id_maladie"],
        "nom_maladie": str(data.get("nom_maladie", "")).strip(),
        "description_maladie": str(data.get("description_maladie", "")).strip(),
        "traitements_recommandes_maladie": str(
            data.get("traitements_recommandes_maladie", "")
        ).strip(),
    }

    # Ajout automatique de tout champ non géré explicitement
    for k, v in data.items():
        if k not in doc:
            doc[k] = v

    return doc
