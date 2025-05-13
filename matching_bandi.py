# Mappatura coerente delle colonne CSV per i bandi pubblici
COLONNE_BANDI = {
    "titolo": "Titolo",
    "descrizione": "Descrizione",
    "finalita": "Obiettivo_Finalita",
    "apertura": "Data_apertura",
    "scadenza": "Data_chiusura",
    "dimensione": "Dimensioni",
    "forma_agevolazione": "Forma_agevolazione",
    "spesa_min": "Spesa_Ammessa_min",
    "spesa_max": "Spesa_Ammessa_max",
    "agevolazione_min": "Agevolazione_Concedibile_min",
    "agevolazione_max": "Agevolazione_Concedibile_max",
    "settore": "Settore_Attivita",
    "ateco": "Codici_ATECO",
    "regione": "Regioni",
    "comune": "Comuni",
    "territorio": "Ambito_territoriale",
    "ente": "Soggetto_Concedente",
    "link": "Link_istituzionale"
}

import csv
from datetime import datetime

def filtra_bandi_compatibili(bandi: list, caratteristiche_azienda: dict) -> list:
    risultati = []
    oggi = datetime.today().date()

    for row in bandi:
        # Controlla se la scadenza è ancora valida
        scadenza_str = row.get(COLONNE_BANDI["scadenza"], "")
        try:
            scadenza = datetime.strptime(scadenza_str, "%Y-%m-%d").date()
            if scadenza < oggi:
                continue  # salta bandi scaduti
        except ValueError:
            pass  # se il formato data non è valido, continua comunque

        ateco_match = caratteristiche_azienda["codice_ateco"] in row.get(COLONNE_BANDI["ateco"], "")
        regione_match = caratteristiche_azienda["regione"].lower() in row.get(COLONNE_BANDI["regione"], "").lower()
        forma_match = caratteristiche_azienda["forma_giuridica"].lower() in row.get(COLONNE_BANDI["descrizione"], "").lower()
        dim_match = caratteristiche_azienda["dimensione_impresa"].lower() in row.get(COLONNE_BANDI["dimensione"], "").lower()

        if ateco_match and regione_match and forma_match and dim_match:
            risultati.append(row)

    return risultati

def carica_bandi_da_csv(percorso: str) -> list:
    with open(percorso, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)

if __name__ == "__main__":
    bandi = carica_bandi_da_csv("dataset_bandi.csv")
    caratteristiche_azienda = {
        "codice_ateco": "62.01",
        "regione": "Lazio",
        "forma_giuridica": "srl",
        "dimensione_impresa": "piccola"
    }
    compatibili = filtra_bandi_compatibili(bandi, caratteristiche_azienda)
    print(f"Bandi compatibili trovati: {len(compatibili)}")
    for b in compatibili:
        print(b.get(COLONNE_BANDI["titolo"], "Senza titolo"))
