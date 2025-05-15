import json
import fitz  # PyMuPDF
import re
import logging

def estrai_dati_da_pdf(percorso_pdf):
    print("📎 Entrata in estrai_dati_da_pdf()")
    try:
        with fitz.open(percorso_pdf) as doc:
            testo = ""
            for pagina in doc:
                testo += pagina.get_text("text")

        logging.info(f"📏 Lunghezza testo PDF: {len(testo)}")
        logging.info(f"🧾 Testo PDF estratto (prime 800c):\n{testo[:800]}")
    except Exception as e:
        logging.error(f"❌ Errore apertura PDF: {e}")
        raise

    caratteristiche_azienda = {
        "forma_giuridica": estrai_valore(testo, r"Forma giuridica[:\s]+(.+?)\n"),
        "codice_ateco": estrai_valore(testo, r"Codice Ateco[:\s]+(.+?)\n"),
        "attivita_prevalente": estrai_valore(testo, r"Attività prevalente[:\s]+(.+?)\n")
        "denominazione": estrai_valore(testo, r"Denominazione[:\s]+(.+?)\n"),
        "amministratore": estrai_valore(testo, r"Amministratore[:\s]+(.+?)\n"),
    }

    bilancio = {
        "totale_attivo": estrai_valore(testo, r"Totale attivo[:\s]+([\d\.]+)"),
        "fatturato": estrai_valore(testo, r"Fatturato[:\s]+([\d\.]+)"),
        "utile_netto": estrai_valore(testo, r"Utile netto[:\s]+([\d\.]+)")
    }

    return caratteristiche_azienda, bilancio

def estrai_valore(testo, pattern):
    match = re.search(pattern, testo)
    return match.group(1).strip() if match else None
