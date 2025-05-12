import requests
import pandas as pd

# URL reale del dataset CSV da MIMIT (aggiornare se cambia)
CSV_URL = "https://www.incentivi.gov.it/opendata/elenco_incentivi.csv"
OUTPUT_PATH = "data/bandi.csv"

def scarica_e_formatta_bandi():
    try:
        df = pd.read_csv(CSV_URL, delimiter=';', encoding='utf-8')
        colonne = {
            'Titolo incentivo': 'titolo',
            'Descrizione incentivo': 'descrizione',
            'Territorio': 'regione',
            'Codici ATECO Ammissibili': 'codice_ateco_ammessi',
            'Fatturato minimo': 'fatturato_minimo',
            'Finalità': 'finalità',
            'Forma di agevolazione': 'tipo_agevolazione',
            'Data scadenza': 'scadenza'
        }
        df_filtrato = df[list(colonne.keys())].rename(columns=colonne)
        df_filtrato.to_csv(OUTPUT_PATH, index=False)
        print("✅ bandi.csv aggiornato con successo.")
    except Exception as e:
        print("❌ Errore durante l'aggiornamento bandi:", e)

if __name__ == "__main__":
    scarica_e_formatta_bandi()
