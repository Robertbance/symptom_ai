# SymptomAI – Chatbot de Diagnostic Médical Préliminaire  

SymptomAI est un chatbot intelligent permettant aux utilisateurs de décrire leurs symptômes en langage naturel et d’obtenir une **évaluation médicale préliminaire** grâce à des techniques de **Traitement du Langage Naturel (NLP)** et de **Machine Learning**.  

⚠️ **Avertissement** : Ce projet est conçu uniquement à des fins pédagogiques et **ne remplace pas un diagnostic médical professionnel**.  

---

## ✨ Fonctionnalités  

- 💬 Saisie des symptômes en langage naturel (Français / Anglais)  
- 🌐 Traduction automatique FR ↔ EN  
- 🧹 Nettoyage linguistique des textes (NLP)  
- 🤖 Prédiction des maladies probables via modèles ML  
- 📊 Calcul d’un score de similarité  
- 🩺 Recommandations médicales préliminaires  
- 🔐 Système d’authentification (inscription / connexion)  
- 📜 Gestion de l’historique des consultations  
- 👤 Profil utilisateur personnalisé  

---

## 🛠️ Technologies utilisées  

- **Backend** : Flask (Python)  
- **Frontend** : HTML, CSS, JavaScript  
- **NLP** : NLTK, SpaCy, Sentence Transformers  
- **Machine Learning** : Scikit-learn (SVM)  
- **Base de données** : MongoDB  
- **Modélisation** : Looping (MLD)  
- **Dataset** : Kaggle (données médicales en anglais)  

---

## 📂 Structure du projet  

```
symptom_ai/
│
├── app.py
├── config.py
├── requirements.txt
│
├── routes/
│   └── chatbot_routes.py
│
├── nlp/
│   ├── preprocess.py
│   ├── translate.py
│   └── correct.py
│
├── database/
│   ├── mongo_connection.py
│   └── queries.py
│
├── models/   (fichiers modèles ignorés sur GitHub)
│
├── static/
└── templates/
```

---

## ⚙️ Installation  

1. **Cloner le projet** :  
```bash
git clone https://github.com/Robertbance/symptom_ai.git
cd symptom_ai
```

2. **Créer un environnement virtuel** :  
```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

3. **Installer les dépendances** :  
```bash
pip install -r requirements.txt
```

4. **Lancer l’application** :  
```bash
python app.py
```

➡️ Ouvrir le navigateur à l’adresse : [http://127.0.0.1:5000](http://127.0.0.1:5000)  

---

## 🚀 Utilisation  

1. Créer un compte (Inscription)  
2. Se connecter  
3. Accéder à l’interface du chatbot  
4. Saisir ses symptômes  
5. Visualiser les prédictions  
6. Consulter l’historique des consultations  

---

## 🧠 Modèles Machine Learning  

Les fichiers de modèles ne sont pas stockés sur GitHub pour des raisons de taille.  
Pour les générer localement :  

1. Ouvrir le notebook Jupyter  
2. Lancer les cellules d’entraînement  
3. Générer les fichiers suivants :  
   - `svm_classifier.pkl`  
   - `sbert_encoder.pkl`  
   - `symptom_embeddings.npy`  
   - `df_index.csv`  

---

## 👨‍💻 Auteur  

**Robert Bancé**  
Licence 3 – Modélisation, Simulation et Calcul Scientifique  
Spécialité: Mathématiques appliqués et modélisation
Université Virtuelle du Burkina Faso  
📧 Email : bancerobert6@gmail.com  
```

