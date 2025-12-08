# nlp/preprocess.py
"""
Prétraitement texte pour le chatbot médical.
Fonctions :
- normalisation
- nettoyage
- lemmatisation
- suppression stopwords
"""

import spacy
import re
import string

# Charger le modèle spaCy français
# Installe-le si nécessaire : python -m spacy download fr_core_news_md
nlp = spacy.load("fr_core_news_md")

# Ponctuation + stopwords
punct = set(string.punctuation)


def normalize_text(text: str) -> str:
    """
    Normalisation simple :
    - convertit en minuscules
    - retire espaces inutiles
    """
    if not isinstance(text, str):
        return ""
    return text.lower().strip()


def clean_text(text: str) -> str:
    """
    Pipeline complet de nettoyage NLP :
    - normalisation
    - tokenisation spaCy
    - suppression stopwords
    - Lemmatisation
    - Filtrage tokens non alphabétiques
    """
    text = normalize_text(text)
    doc = nlp(text)

    tokens = []
    for token in doc:
        if token.is_alpha and not token.is_stop:
            lemma = token.lemma_.strip()
            if lemma:
                tokens.append(lemma)

    return " ".join(tokens)
