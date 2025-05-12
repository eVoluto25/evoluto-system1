import requests
import csv
import json
import os

def download_bandi():
    # URL dei dataset CSV (aggiungi il link del secondo sito)
    urls = [
        "https://www.incentivi.gov.it/it/open-data",
        "https://www.ponic.gov.it/open-data/datasets"
    ]

    for url in urls:
        # Scarica il file CSV dal sito
        response = requests.get(url)

        # Verifica se il download è stato completato con successo
        if response.status_code == 200:
            # Salva il CSV scaricato nella directory corrente
            file_name = url.split('/')[-1] + '.csv'  # Usa il nome dell'URL per salvare il file
            with open(file_name, "wb") as file:
                file.write(response.content)
                print(f"CSV scaricato con successo da {url}!")
        else:
            print(f"Errore nel download del file {url}: {response.status_code}")
