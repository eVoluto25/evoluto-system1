import json
import fitz  # PyMuPDF
import re
import logging

def estrai_dati_da_pdf(percorso_pdf):
    try:
        with fitz.open(percorso_pdf) as doc:
            testo = ""
            for pagina in doc:
                testo += pagina.get_text()

        logging.info(f"📄 Testo PDF estratto (prime 800c):\n{text[:800]}")
    except Exception as e:
        logging.error(f"❌ Errore apertura PDF: {e}")
        raise

    caratteristiche_azienda = {
        "forma_giuridica": estrai_valore(testo, r"Forma giuridica[:\s]+(.+?)\n"),
        "codice_ateco": estrai_valore(testo, r"Codice Ateco[:\s]+(.+?)\n"),
        "attivita_prevalente": estrai_valore(testo, r"Attività prevalente[:\s]+(.+?)\n")
    }

    bilancio = {
        "ricavi": estrai_valore(testo, r"Ricavi[:\s]+([0-9\.,]+)"),
        "ebitda": estrai_valore(testo, r"EBITDA[:\s]+([0-9\.,]+)"),
        "utile_netto": estrai_valore(testo, r"Utile netto[:\s]+([0-9\.,]+)"),
        "attivo_totale": estrai_valore(testo, r"Attivo totale[:\s]+([0-9\.,]+)"),
        "patrimonio_netto": estrai_valore(testo, r"Patrimonio netto[:\s]+([0-9\.,]+)")
    }

    logging.info(f"➡️ Caratteristiche azienda: {caratteristiche_azienda}")
    logging.info(f"➡️ Bilancio: {bilancio}")

    with open("caratteristiche_azienda.json", "w") as f:
        json.dump(caratteristiche_azienda, f, indent=2)

    return caratteristiche_azienda, bilancio

def estrai_valore(testo, pattern):
    match = re.search(pattern, testo, re.IGNORECASE)
    return match.group(1).strip() if match else "N/D"
