import json
import requests
import logging
import csv
from datetime import datetime

# Configurazione esempio - puoi caricarla da config_siti_bandi.json se preferisci
FONTI = [
    {
        "nome": "Regione Lazio",
        "url": "https://opendata.regione.lazio.it/bandi.csv",
        "formato": "csv"
    },
    {
        "nome": "Invitalia",
        "url": "https://www.invitalia.it/opendata/bandi.json",
        "formato": "json"
    }
]

def aggiorna_bandi():
    bandi_totali = []

    for fonte in FONTI:
        logging.info(f"📥 Scaricamento bandi da {fonte['nome']}...")

        try:
            r = requests.get(fonte["url"], timeout=10)
            r.raise_for_status()

            if fonte["formato"] == "csv":
                bandi = parse_csv(r.text)
            elif fonte["formato"] == "json":
                bandi = parse_json(r.json())
            else:
                logging.warning(f"⚠️ Formato non riconosciuto: {fonte['formato']}")
                bandi = []

            logging.info(f"✅ {len(bandi)} bandi estratti da {fonte['nome']}")
            bandi_totali.extend(bandi)

        except Exception as e:
            logging.error(f"❌ Errore durante il download da {fonte['nome']}: {e}")

    # Salva nel file principale
    with open("bandi_bandi.json", "w", encoding="utf-8") as f:
        json.dump(bandi_totali, f, indent=2, ensure_ascii=False)

    logging.info(f"📦 Totale bandi salvati: {len(bandi_totali)}")

def parse_csv(contenuto_csv):
    righe = csv.DictReader(contenuto_csv.splitlines())
    bandi = []
    for r in righe:
        bandi.append({
            "titolo": r.get("Titolo", "N/D"),
            "beneficiari": r.get("Beneficiari", ""),
            "settori": r.get("Settori", ""),
            "ateco": r.get("Codice ATECO", ""),
            "forma_agevolazione": r.get("Tipologia", ""),
            "scadenza": r.get("Data Scadenza", ""),
            "fonte": "CSV"
        })
    return bandi

def parse_json(lista_json):
    bandi = []
    for b in lista_json:
        bandi.append({
            "titolo": b.get("titolo", "N/D"),
            "beneficiari": b.get("beneficiari", ""),
            "settori": b.get("settori", ""),
            "ateco": b.get("ateco", ""),
            "forma_agevolazione": b.get("forma_agevolazione", ""),
            "scadenza": b.get("scadenza", ""),
            "fonte": "JSON"
        })
    return bandi
