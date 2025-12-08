# SymptomAI – Chatbot de Diagnostic Médical Préliminaire

SymptomAI est un chatbot intelligent développé dans un cadre académique. Il permet aux utilisateurs de décrire leurs symptômes en langage naturel et d’obtenir une évaluation médicale préliminaire basée sur des techniques de Traitement du Langage Naturel (NLP) et de Machine Learning.

Ce projet est conçu uniquement à des fins pédagogiques et ne remplace pas un diagnostic médical professionnel.

---

## Fonctionnalités

- Saisie des symptômes en langage naturel (français / anglais)
- Traduction automatique FR → EN et EN → FR
- Nettoyage linguistique des textes (NLP)
- Prédiction des maladies probables
- Calcul d’un score de similarité
- Recommandations médicales préliminaires
- Système d’authentification (inscription / connexion)
- Gestion de l’historique des consultations
- Profil utilisateur

---

## Technologies utilisées

- Backend : Flask (Python)
- Frontend : HTML, CSS, JavaScript
- NLP : NLTK, SpaCy, Sentence Transformers
- Machine Learning : Scikit-learn (SVM)
- Base de données : MongoDB
- Outil de modélisation : Looping (MLD)
- Dataset : Kaggle (données médicales en anglais)

---

## Structure du projet

symptom_ai/

│

├── app.py

├── config.py

├── requirements.txt

├── routes/

│ └── chatbot_routes.py

├── nlp/

│ ├── preprocess.py

│ ├── translate.py

│ └── correct.py

├── database/

│ ├── mongo_connection.py

│ └── queries.py

├── models/

│ └── (fichiers modèles ignorés sur GitHub)

├── static/

└── templates/


---

## Installation

1. Cloner le projet :

```bash
git clone https://github.com/Robertbance/symptom_ai.git
cd symptom_ai

## Environnement virtuel

python -m venv venv
venv\Scripts\activate

## Installation des dépendances
pip install -r requirements.txt

## Lancement de l'application
python app.py

Puis ouvrir le navigateur à l’adresse :
http://127.0.0.1:5000

---

# Utilisation

- Créer un compte (Inscription)

- Se connecter

- Accéder à l’interface du chatbot

- Saisir ses symptômes

- Visualiser les prédictions

- Consulter l’historique

---

# Modèles Machine Learning
Pour des raisons de taille, les fichiers de modèles ne sont pas stockés sur GitHub.

Pour les générer localement :

    -Ouvrir le notebook Jupyter

    -Lancer les cellules d’entraînement

    -Générer :

      -svm_classifier.pkl

      -sbert_encoder.pkl

      -symptom_embeddings.npy

      -df_index.csv

---

# Auteur

Robert Bancé
Licence 3 – Modélisation, Simulation et Calcul Scientifique
Université Virtuelle du Burkina Faso
Adresse email: bancerobert6@gmail.com




