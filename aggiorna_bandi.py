import os
import requests
import csv
from datetime import datetime

DATASET_URL = "https://www.incentivi.gov.it/sites/default/files/open-data/2025-4-5_opendata-export.csv"
DATASET_FILE = "dataset_bandi.csv"
ETAG_FILE = ".etag_cache.txt"


def file_aggiornato(url, cache_path):
    response = requests.head(url, timeout=10)
    nuovo_etag = response.headers.get("ETag") or response.headers.get("Last-Modified")

    etag_precedente = None
    if os.path.exists(cache_path):
        with open(cache_path, "r") as f:
            etag_precedente = f.read().strip()

    if nuovo_etag != etag_precedente:
        with open(cache_path, "w") as f:
            f.write(nuovo_etag)
        return True
    return False


def scarica_file(url, destinazione):
    response = requests.get(url, timeout=30)
    with open(destinazione, "wb") as f:
        f.write(response.content)
    print(f"✅ File aggiornato scaricato in {destinazione}")


def formatta_bandi():
    if file_aggiornato(DATASET_URL, ETAG_FILE):
        scarica_file(DATASET_URL, DATASET_FILE)
    else:
        print("⏭️ Nessun aggiornamento disponibile. Dataset invariato.")


if __name__ == "__main__":
    aggiorna_bandi()
