
from datetime import datetime
from typing import Dict, Any

# Champs strictement obligatoires
REQUIRED_FIELDS = [
    "id_user",
    "nom_user",
    "prenom_user",
    "email_user",
    "sexe_user",
    "age_user"
]


def build_user_document(data: Dict[str, Any]) -> Dict[str, Any]:
    # Vérification des champs obligatoires
    missing = [field for field in REQUIRED_FIELDS if field not in data]
    if missing:
        raise ValueError(f"Champs obligatoires manquants : {missing}")

    # Normalisation des champs

    # id_user → string (IMPÉRATIF pour compatibilité totale avec tes queries)
    id_user = str(data["id_user"]).strip()

    nom = str(data.get("nom_user", "")).strip()
    prenom = str(data.get("prenom_user", "")).strip()

    email = data.get("email_user", "")
    email = str(email).strip().lower()  # email toujours en minuscule

    sexe = str(data.get("sexe_user", "")).strip()

    # âge → converti en entier + protection type
    try:
        age = int(data.get("age_user"))
    except Exception:
        raise ValueError("Le champ age_user doit être un entier.")

    # date inscription → datetime automatique si absent
    date_inscrit = data.get("date_inscrit_user")
    if not isinstance(date_inscrit, datetime):
        date_inscrit = datetime.utcnow()

    # Construction du document final
    user = {
        "id_user": id_user,
        "nom_user": nom,
        "prenom_user": prenom,
        "email_user": email,
        "sexe_user": sexe,
        "age_user": age,
        "date_inscrit_user": date_inscrit,
    }

    # Ajout des champs supplémentaires éventuels
    # (ex : adresse, téléphone, etc.)
    # ------------------------------
    for k, v in data.items():
        if k not in user:
            user[k] = v

    return user
