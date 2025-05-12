import pandas as pd

def carica_bandi(csv_path):
    return pd.read_csv(csv_path)

def filtra_bandi_compatibili(bandi_df, caratteristiche_impresa):
    compatibili = []
    for _, bando in bandi_df.iterrows():
        if (caratteristiche_impresa["forma_agevolazione"] in bando["forma_agevolazione"]
            and caratteristiche_impresa["territorio"] in bando["territorio"]
            and caratteristiche_impresa["beneficiari"] in bando["beneficiari"]
            and caratteristiche_impresa["finalita"] in bando["finalita"]):
            compatibili.append(bando.to_dict())
    return compatibili
