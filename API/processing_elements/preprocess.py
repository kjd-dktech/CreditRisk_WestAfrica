import pandas as pd
import numpy as np
import joblib
from loguru import logger

# Chargement des éléments
encoder = joblib.load("API/processing_elements/Hot_encoder.pkl")
scaler = joblib.load("API/processing_elements/scaler.pkl")
features = joblib.load("API/processing_elements/feature_list.pkl")
loan_type_dtype = joblib.load("API/processing_elements/loan_type_dtype.pkl")


EXPECTED_LOAN_TYPES = ['short_term', 'long_term', 'microcredit']
EXPECTED_REPEAT = ['new', 'repeat']

def preprocessor(input_data: pd.DataFrame):
    """
    Transforme une entrée brute en vecteur prêt pour la prédiction
    """

    logger.info("🧪 Preprocessing started")
    df = input_data.copy()

    try :
        # Vérifications de base
        required_columns = [
            "Total_Amount", "Total_Amount_to_Repay", "Amount_Funded_By_Lender",
            "duration", "Lender_portion_to_be_repaid", "loan_type"
        ]
        missing_cols = set(required_columns) - set(df.columns)
        if missing_cols:
            raise ValueError(f"Colonnes manquantes : {missing_cols}")

        # Conversion des types
        df['loan_type'] = df['loan_type'].astype(loan_type_dtype)
        # Vérifie s'il y a des valeurs inconnues
        if df['loan_type'].isna().any():
            raise ValueError(f"Valeur(s) inconnue(s) dans 'loan_type' : {df['loan_type'][df['loan_type'].isna()]}")
        
        #df["New_versus_Repeat"] = df["New_versus_Repeat"].astype(str).str.lower().str.strip()


        # Feature engineering
        df["repayment_ratio"] = df["Total_Amount_to_Repay"] / df["Total_Amount"]
        df["repayment_ratio"] = df["repayment_ratio"].replace([np.inf, -np.inf], np.nan)
        

        # Encodage OneHot sur New_versus_Repeat
        #encoded_var = pd.DataFrame(
        #    encoder.transform(df[['New_versus_Repeat']]).toarray(),
        #    columns=encoder.get_feature_names_out(['New_versus_Repeat']),
        #    index=df.index
        #)
        #df = pd.concat([df.drop(columns=['New_versus_Repeat']), encoded_var], axis=1)

        # Encodage loan_type
        df['loan_type_encoded'] = df['loan_type'].cat.codes
        df.drop(columns=['loan_type'], inplace=True)

        # Sélection les features dans l’ordre exact
        try:
            df = df[features]
        except KeyError as e:
            missing = list(set(features) - set(df.columns))
            raise ValueError(f"Colonnes manquantes dans les données d'entrée : {missing}")


        # Gestion des potentiels NaN
        df.fillna(0, inplace=True)

        # Standardisation
        df_scaled = scaler.transform(df)

        logger.info("✅ Preprocessing completed")

        return pd.DataFrame(df_scaled, columns=df.columns, index=df.index)
    
    except Exception as e:
        logger.exception("❌ Preprocessing failed")
        raise

