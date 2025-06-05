from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
import pandas as pd
import shap
from '../API/processing_elements/preprocess' import preprocessor


#preprocessor = joblib.load("../API/processing_elements/preprocessor.pkl")
# Chargement du modèle
model = joblib.load("../API/models/stacking_model.pkl")

# Chargement de l'explainer SHAP
explainer = joblib.load("../API/shap_explainer/explainer.pkl")

app = FastAPI(title="Credit Scoring API")

class LoanProfile(BaseModel):
    Total_Amount: float
    Total_Amount_to_Repay : float
    Amount_Funded_By_Lender: float
    duration: int
    Lender_portion_to_be_repaid: float
    loan_type: str

@app.post("/predict")
def predict(profile: LoanProfile):
    df = pd.DataFrame([profile.dict()])
    df_preprocessed = preprocessor(df)

    proba = model.predict_proba(df_preprocessed)[0][1]
    pred = int(proba >= 0.5)
    return {"probability": proba, "prediction": pred}

@app.post("/explain")
def explain(profile: LoanProfile):
    df = pd.DataFrame([profile.dict()])
    df_preprocessed = preprocessor(df)

    shap_values = explainer(df_preprocessed)
    base_value = explainer.expected_value
    feature_contribs = dict(zip(df.columns, shap_values[0].values))

    return {
        "base_value": base_value,
        "contributions": feature_contribs,
        "prediction": model.predict(df_preprocessed)[0]
    }
