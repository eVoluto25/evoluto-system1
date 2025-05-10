import requests
import csv
import json
import os

def download_bandi():
    # URL del dataset CSV (sostituisci con il link corretto)
    url = "https://www.incentivi.gov.it/it/open-data"
    
    # Scarica il file CSV dal sito
    response = requests.get(url)
    
    # Verifica se il download è stato completato con successo
    if response.status_code == 200:
        # Salva il CSV scaricato nella directory corrente
        with open("dataset_mimit.csv", "wb") as file:
            file.write(response.content)
        print("CSV scaricato con successo!")
    else:
        print(f"Errore nel download del file: {response.status_code}")

def parse_mimit_csv():
    input_path = "dataset_mimit.csv"
    output_path = "bandi_mimit.json"
    bandi = []

    try:
        # Verifica se il file CSV esiste
        if not os.path.exists(input_path):
            raise Exception(f"File {input_path} non trovato.")
        
        # Apre il file CSV per il parsing
        with open(input_path, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                codice = row.get("ID_Incentivo")  # Assicurati che la colonna sia corretta
                titolo = row.get("Titolo")  # Assicurati che la colonna sia corretta
                bandi.append({"codice": codice, "titolo": titolo})

        # Salva i dati in formato JSON
        with open(output_path, mode="w", encoding="utf-8") as output_file:
            json.dump(bandi, output_file, ensure_ascii=False, indent=4)
        print("File JSON creato con successo!")

    except Exception as e:
        print(f"Errore nella lettura del CSV o scrittura del JSON: {e}")

# Esegui le funzioni di download e parsing
download_bandi()
parse_mimit_csv()
