# models/diagnostic_model.py
"""
Schéma et helpers pour la collection 'diagnostic'.
Assure une validation robuste et une structure cohérente des documents.
"""

from datetime import datetime
from typing import Dict, Any, List


REQUIRED_FIELDS = ["id_diagnostic", "id_user", "id_maladie"]


def build_diagnostic_document(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Construit et valide un document 'diagnostic' conforme à MongoDB.

    ✔ id_user, id_maladie, id_diagnostic → forcés en string
    ✔ date_diagnostic → auto si absente
    ✔ confiance_diagnostic → float sécurisé
    ✔ recommandations_diagnostic → nettoyé
    ✔ symptomes → liste normalisée de dicts {nom_symptome: "..."}
    """

    # -------------------------------------------------------
    # 1️⃣ Vérification des champs obligatoires
    # -------------------------------------------------------
    missing = [field for field in REQUIRED_FIELDS if field not in data]
    if missing:
        raise ValueError(f"Champs obligatoires manquants : {missing}")

    # -------------------------------------------------------
    # 2️⃣ Normalisation des types essentiels
    # -------------------------------------------------------
    id_diag = str(data["id_diagnostic"]).strip()
    id_user = str(data["id_user"]).strip()
    id_maladie = str(data["id_maladie"]).strip()

    # -------------------------------------------------------
    # 3️⃣ Date du diagnostic
    # -------------------------------------------------------
    date_diag = data.get("date_diagnostic")
    if not isinstance(date_diag, datetime):
        date_diag = datetime.utcnow()

    # -------------------------------------------------------
    # 4️⃣ Confiance du diagnostic
    # -------------------------------------------------------
    try:
        confiance = float(data.get("confiance_diagnostic", 0.0))
    except Exception:
        confiance = 0.0

    # -------------------------------------------------------
    # 5️⃣ Recommandations
    # -------------------------------------------------------
    recommandations = str(data.get("recommandations_diagnostic", "")).strip()

    # -------------------------------------------------------
    # 6️⃣ Symptômes
    # Acceptés :
    #   - liste de strings  → ["fièvre", "toux"]
    #   - liste obj légers → [{"nom_symptome":"fièvre"}]
    # -------------------------------------------------------
    symptomes = data.get("symptomes", [])

    if not isinstance(symptomes, list):
        raise ValueError("Le champ 'symptomes' doit être une liste.")

    normalized_symptomes: List[Dict[str, str]] = []

    for s in symptomes:
        if isinstance(s, dict) and "nom_symptome" in s:
            # déjà bien structuré
            normalized_symptomes.append({
                "nom_symptome": str(s["nom_symptome"]).strip()
            })

        elif isinstance(s, str):
            # symptôme simple → converti en structure
            normalized_symptomes.append({"nom_symptome": s.strip()})

        else:
            raise ValueError(
                "Chaque symptôme doit être une string ou un dict {nom_symptome: ...}"
            )

    # -------------------------------------------------------
    # 7️⃣ Construction finale du document
    # -------------------------------------------------------
    doc = {
        "id_diagnostic": id_diag,
        "date_diagnostic": date_diag,
        "confiance_diagnostic": confiance,
        "recommandations_diagnostic": recommandations,
        "id_maladie": id_maladie,
        "id_user": id_user,
        "symptomes": normalized_symptomes
    }

    # -------------------------------------------------------
    # 8️⃣ Ajout des champs optionnels non gérés explicitement
    # -------------------------------------------------------
    for key, value in data.items():
        if key not in doc:
            doc[key] = value

    return doc
