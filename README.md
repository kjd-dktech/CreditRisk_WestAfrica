# CreditRisk West Africa

Modélisation prédictive du risque de crédit pour l'inclusion financière en Afrique de l'Ouest.

## Objectif

Ce projet vise à développer un système intelligent capable d’évaluer automatiquement la solvabilité d’un demandeur de crédit, afin de soutenir l’inclusion financière des petites entreprises et agriculteurs dans la région.

## Fonctionnalités

- Analyse exploratoire des données (EDA)
- Préparation et nettoyage des données
- Modélisation prédictive (RandomForest, XGBoost, Logistic Regression, Stacking)
- Interprétabilité des modèles (SHAP)
- API REST pour la prédiction et l'explication des décisions
- Visualisations et rapports automatisés (HTML, PDF, slides)

## Structure du projet

```
.
├── API/                  # Code de l'API FastAPI, modèles ML, preprocessing, logs
├── Data/                 # Jeux de données (train, test, economic indicators, etc.)
├── Docs/                 # Documentation, rapports, slides, images
├── Models/               # Modèles sauvegardés
├── Notebook/             # Notebooks d'analyse, modélisation, interprétation
├── Src/                  # (optionnel) Code source additionnel
├── logs/                 # Logs d'exécution
├── docker-compose.yml    # Déploiement Docker
├── promtail-config.yaml  # Config pour la collecte de logs
├── requirements.txt      # Dépendances Python
├── README.md             # Ce fichier
├── .gitignore            # Fichiers/rep à ignorer par git
└── .env                  # Variables d'environnement (API keys, etc.)
```

## Installation

1. **Cloner le repo :**
   ```sh
   git clone https://github.com/<ton-user>/CreditRisk_WestAfrica.git
   cd CreditRisk_WestAfrica
   ```

2. **Créer un environnement virtuel :**
   ```sh
   python3 -m venv creditriskwestafricavenv
   source creditriskwestafricavenv/bin/activate
   ```

3. **Installer les dépendances :**
   ```sh
   pip install -r requirements.txt
   ```

4. **Configurer l'environnement :**
   - Copier `.env.example` en `.env` et adapter les variables si besoin.

## Utilisation

### 1. Analyse et Modélisation

- Ouvre et exécute le notebook principal :
  ```
  Notebook/book.ipynb
  ```
- Les rapports sont générés automatiquement dans `Docs/Rapport/`.

### 2. API de prédiction

- Lancer l'API :
  ```sh
  cd API
  uvicorn main:app --reload
  ```
- Accéder à la documentation interactive : [http://localhost:8000/docs](http://localhost:8000/docs)

### 3. Génération des rapports

- Depuis le notebook :
  ```python
  !jupyter nbconvert --to html book.ipynb --output ../Docs/Rapport/book.html --allow-errors
  !jupyter nbconvert --to pdf book.ipynb --output ../Docs/Rapport/book.pdf --allow-errors
  !jupyter nbconvert --to slides book.ipynb --output ../Docs/Rapport/book.slides.html --no-prompt --no-input --allow-errors
  ```

## Technologies

- Python, Pandas, Scikit-learn, XGBoost, Imbalanced-learn, SHAP
- FastAPI
- Docker
- Jupyter Notebook

## Auteurs

- Kodjo Jean DEGBEVI

## Licence

Projet académique, voir le fichier LICENSE si présent.
