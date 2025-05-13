import csv
import logging

def carica_bandi(csv_path):
    try:
        with open(csv_path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            bandi = [row for row in reader if isinstance(row, dict)]
            logging.info(f"✅ Caricati {len(bandi)} bandi dal file CSV")
            return bandi
    except Exception as e:
        logging.error(f"Errore nel caricamento bandi: {e}")
        return []

def filtra_bandi_compatibili(bandi, caratteristiche_impresa):
    bandi_compatibili = []

    for bando in bandi:
        if not isinstance(bando, dict):
            logging.warning(f"⚠️ Riga non valida, ignorata: {bando}")
            continue

        try:
            territorio = bando.get("territorio", "").lower()
            beneficiari = bando.get("beneficiari", "").lower()
            finalita = bando.get("finalita", "").lower()

            if (
                caratteristiche_impresa.get("territorio", "").lower() in territorio
                and caratteristiche_impresa.get("forma_giuridica", "").lower() in beneficiari
                and caratteristiche_impresa.get("obiettivo", "").lower() in finalita
            ):
                bandi_compatibili.append(bando)
        except Exception as e:
            logging.error(f"Errore nel filtraggio dei bandi: {e}")
            continue

    logging.info(f"✅ Trovati {len(bandi_compatibili)} bandi compatibili")
    return bandi_compatibili
