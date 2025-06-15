# 🧠 Credit Risk Scoring API

API FastAPI pour évaluer le risque de crédit à partir de caractéristiques de prêts.

## 🚀 Déploiement

L’API est automatiquement déployée sur Render grâce au fichier `.render.yml` à la racine du projet.

➡️ Accès : `https://creditrisk-api.onrender.com/docs`

### Déploiement Render

Le déploiement sur Render se fait automatiquement à chaque push sur la branche principale, selon la configuration du fichier [`CreditRisk_WestAfrica/.render.yml`](../.render.yml).  
Aucune action manuelle n'est requise : Render installe les dépendances, configure les variables d'environnement et lance l'API avec Uvicorn.

**Pour personnaliser le déploiement :**
- Modifiez le fichier `.render.yml` selon vos besoins (dépendances, commandes, variables d'environnement).
- Les secrets/API keys doivent être définis dans le dashboard Render (onglet Environment).

## 📦 Installation locale

```bash
git clone https://github.com/<ton-user>/<ton-repo>.git
cd <ton-repo>
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

## 🔑 Sécurité

- L’API nécessite une clé API (`X-API-Key`) pour accéder aux endpoints critiques.
- Configurez vos variables d’environnement dans `.env` (local) ou via le dashboard Render (production).

## 📚 Documentation interactive

Accédez à la documentation Swagger :  
`https://creditrisk-api.onrender.com/docs`

## 🗂️ Organisation

```
API/
├── main.py                  # Entrée principale FastAPI
├── processing_elements/     # Encoders, scaler, features, dtype sauvegardés
├── ml_models/               # Modèle stacking et pipelines individuels
├── shap_explainer/          # Explainer SHAP sauvegardé
├── logs/                    # Logs d’exécution de l’API
├── utils.py                 # Fonctions utilitaires
├── requirements.txt         # Dépendances Python
├── README.md                # Ce fichier
```

## ✉️ Auteur

Kodjo Jean DEGBEVI

---

Pour toute question, se référer à la documentation du projet principal ou ouvrir une issue sur GitHub.