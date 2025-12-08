"""
Schéma et helpers pour la collection 'symptome'.
"""

from typing import Dict, Any

# Champs pour créer un symptôme
REQUIRED_FIELDS = ["id_symptome", "nom_symptome"]


def build_symptome_document(data: Dict[str, Any]) -> Dict[str, Any]:


    # Vérifier les champs obligatoires
    missing = [field for field in REQUIRED_FIELDS if field not in data]
    if missing:
        raise ValueError(f"Champs obligatoires manquants : {missing}")

    #  Normalisation : convertir ID en string
    id_symptome = str(data["id_symptome"]).strip()

    # Nom du symptôme : netoyage
    nom = str(data.get("nom_symptome", "")).strip()

    #  Description
    description = data.get("description_symptome", "")
    if not isinstance(description, str):
        description = str(description)
    description = description.strip()

    # Construction du document final
    return {
        "id_symptome": id_symptome,
        "nom_symptome": nom,
        "description_symptome": description
    }
