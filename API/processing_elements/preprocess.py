import pandas as pd
import joblib

# Charger scaler et liste des colonnes
encoder = joblib.load("../API/processing_elements/Hot_encoder.pkl")
scaler = joblib.load("../API/processing_elements/scaler.pkl")
features = joblib.load("../API/processing_elements/feature_list.pkl")

def preprocessor(input_data: pd.DataFrame):
    """
    Prend un dictionnaire JSON en entrée et retourne un vecteur prêt à être utilisé par le modèle
    """

    # Dérive des features
    df['repayment_ratio'] = df['Total_Amount_to_Repay'].divide(df['Total_Amount'])


    # Encodage des variables catégorielles
    encoded_var= pd.DataFrame(encoder.transform(df[['New_versus_Repeat']]).toarray(), columns=encoder.get_feature_names_out(['New_versus_Repeat']))
    df = (pd.concat([df, encoded_var], axis=1)).drop(columns=['New_versus_Repeat'])

    df['loan_type_encoded'] = df['loan_type'].astype('category').cat.codes
    df.drop(columns=['loan_type'], inplace=True)


    # Sélectionner les colonnes nécessaires
    df = df[features]

    #pipeline = Pipeline('preprocessor', ColumnTransformer(transformers=[('scaler', scaler, df.columns)]))
    #return pipeline

    # Normaliser
    df_scaled = scaler.transform(df)

    return df_scaled
