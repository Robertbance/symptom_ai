# routes/chatbot_routes.py
from flask import Blueprint, request, jsonify
import joblib, os, uuid
import numpy as np
import pandas as pd

from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

from database.queries import create_diagnostic
from nlp.preprocess import clean_text
from nlp.translate import translate_fr_en, translate_en_fr
from nlp.correct import correct_spelling

chatbot_bp = Blueprint("chatbot", __name__)

MODEL_DIR = "models"

# Chemins des fichiers nécessaires
SVM_PATH = os.path.join(MODEL_DIR, "svm_classifier.pkl")
EMB_PATH = os.path.join(MODEL_DIR, "symptom_embeddings.npy")
DF_PATH = os.path.join(MODEL_DIR, "df_index.csv")

# Chargement des fichiers légers
svm = joblib.load(SVM_PATH)
embeddings = np.load(EMB_PATH)
df_index = pd.read_csv(DF_PATH)

# Chargement SBERT directement depuis Hugging Face (plus besoin de fichier local)
encoder = SentenceTransformer("sentence-transformers/paraphrase-multilingual-mpnet-base-v2")


@chatbot_bp.route("/predict", methods=["POST"])
def predict():
    payload = request.get_json(force=True)
    texte = payload.get("symptome", "")
    user_id = payload.get("id_user")

    if not texte:
        return jsonify({"error": "Le champ 'symptome' est requis"}), 400

    # Traduction FR → EN
    text_en = translate_fr_en(texte)

    # Correction orthographique
    try:
        text_corrected = correct_spelling(text_en)
    except:
        text_corrected = text_en

    # Nettoyage du texte
    text_clean = clean_text(text_corrected)

    # Contrôle du nombre minimum de mots
    if len(text_clean.split()) < 2:
        return jsonify({
            "maladie_predite": "Aucune maladie identifiée — informations insuffisantes",
            "similarite_max": 0,
            "diagnostic_reference": (
                "Les informations fournies ne permettent pas d’établir une analyse fiable. "
                "Merci de préciser davantage vos symptômes."
            )
        }), 200

    # Calcul du score de recouvrement des mots
    user_words = set(text_clean.split())
    df_index["overlap_score"] = df_index["symptomes"].apply(
        lambda x: len(user_words.intersection(str(x).split()))
    )
    overlap_max = df_index["overlap_score"].max()

    # Encodage SBERT de la requête utilisateur
    user_vec = encoder.encode([text_clean])

    # Calcul de similarité cosinus
    sims = cosine_similarity(user_vec, embeddings)[0]
    best_idx = sims.argsort()[-3:][::-1]
    best_similarity = sims[best_idx[0]]

    # Seuils dynamiques de confiance
    dynamic_threshold = max(np.percentile(sims, 95), 0.30)
    low_conf = dynamic_threshold * 0.50
    medium_conf = dynamic_threshold * 0.70

    # Cas de très faible confiance
    if best_similarity < low_conf or overlap_max == 0:
        return jsonify({
            "maladie_predite": None,
            "similarite_max": round(float(best_similarity), 3),
            "exemple_symptome": "",
            "diagnostic_reference": (
                "Je ne parviens pas à interpréter vos symptômes avec précision. "
                "Merci de fournir plus de détails."
            )
        }), 200

    # Cas de confiance moyenne
    if low_conf <= best_similarity < medium_conf:
        return jsonify({
            "maladie_predite": None,
            "similarite_max": round(float(best_similarity), 3),
            "exemple_symptome": "",
            "diagnostic_reference": (
                "Pour une analyse plus fiable, merci de préciser vos symptômes."
            )
        }), 200

    # Cas de forte confiance
    idx = best_idx[0]

    maladie_en = df_index.iloc[idx]["maladies"]
    sympt_en = df_index.iloc[idx]["symptomes"]
    diag_en = df_index.iloc[idx]["diagnostics"]

    # Traduction EN → FR
    maladie_fr = translate_en_fr(maladie_en)
    sympt_fr = translate_en_fr(sympt_en)
    diag_fr = translate_en_fr(diag_en)

    # Réponse
    response = {
        "maladie_predite": maladie_fr,
        "similarite_max": round(float(best_similarity), 3),
        "exemple_symptome": sympt_fr,
        "diagnostic_reference": diag_fr
    }

    # Sauvegarde en base
    try:
        doc = {
            "id_diagnostic": str(uuid.uuid4()),
            "date_diagnostic": pd.Timestamp.now().to_pydatetime(),
            "confiance_diagnostic": float(best_similarity),
            "recommandations_diagnostic": diag_fr,
            "id_maladie": maladie_fr,
            "id_user": user_id,
            "symptomes": [{"nom_symptome": texte}]
        }
        create_diagnostic(doc)
    except Exception as e:
        print("Erreur MongoDB :", e)

    return jsonify(response), 200
