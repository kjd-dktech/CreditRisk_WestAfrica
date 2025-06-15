import os
import sys
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Header, Depends
from pydantic import BaseModel
import joblib
import pandas as pd

from prometheus_fastapi_instrumentator import Instrumentator

from API.processing_elements.preprocess import preprocessor
from API.utils.slack_alert import send_slack_alert
from API.utils.email_alert import send_email_alert

#from API.data_models.schemas import LoanProfile
from API.config.logging_config import logger



load_dotenv()
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '..')))

API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise ValueError("API_KEY not set in environment variables")

SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

#preprocessor = joblib.load("API/processing_elements/preprocessor.pkl")
# Chargement du modèle
model = joblib.load("API/ml_models/stacking_model.pkl")

# Chargement de l'explainer SHAP
explainer = joblib.load("API/shap_explainer/explainer.pkl")


app = FastAPI(title="Credit Scoring API")


instrumentator = Instrumentator().instrument(app).expose(app)

def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")


class LoanProfile(BaseModel):
    Total_Amount: float
    Total_Amount_to_Repay : float
    Amount_Funded_By_Lender: float
    duration: int
    Lender_portion_to_be_repaid: float
    loan_type: str

@app.get("/")
def root():
    logger.info("Root endpoint hit ✅")
    return {"message": "API OK"}

@app.post("/predict")
def predict(profile: LoanProfile, auth=Depends(verify_api_key)):
    try:
        df = pd.DataFrame([profile.model_dump()])
        logger.info(f"Received predict request: {df.to_dict(orient='records')}")
        
        df_preprocessed = preprocessor(df)
        proba = model.predict_proba(df_preprocessed)[0][1]
        pred = int(proba >= 0.5)
        
        logger.success(f"Prediction made: Probability={proba}, Class={pred}")
        return {"probability": proba, "prediction": pred}
    except Exception as e:
        logger.error(f"Prediction failed: {e}", exc_info=True)
        send_slack_alert(f"❗ Predict Error: {e}")
        send_email_alert("Erreur /predict", str(e))
        raise HTTPException(status_code=500, detail="Prediction error")

@app.post("/explain")
def explain(profile: LoanProfile, auth=Depends(verify_api_key)):
    try:
        df = pd.DataFrame([profile.model_dump()])
        logger.info(f"Received explain request: {df.to_dict(orient='records')}")
        
        df_preprocessed = preprocessor(df)
        shap_values = explainer.shap_values(df_preprocessed)

        # Gestion du format des SHAP values
        if isinstance(shap_values, list):
            shap_vector = shap_values[1][0]
        else:
            shap_vector = shap_values[0]

        feature_contribs = {str(k): float(v) for k, v in zip(df.columns, shap_vector)}

        base_value = explainer.expected_value
        if isinstance(base_value, list):
            base_value = float(base_value[1])
        else:
            base_value = float(base_value)

        prediction = int(model.predict(df_preprocessed)[0])
        logger.info(f"Explanation computed, prediction: {prediction}")
        
        return {
            "base_value": base_value,
            "contributions": feature_contribs,
            "prediction": prediction
        }
    except Exception as e:
        logger.error(f"Explanation failed: {e}", exc_info=True)
        send_slack_alert(f"❗ Explain Error: {e}")
        send_email_alert("Erreur /explain", str(e))
        raise HTTPException(status_code=500, detail="Explanation error")
    