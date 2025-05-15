import json
import fitz  # PyMuPDF
import re
import logging

def estrai_dati_da_pdf(percorso_pdf):
    print("📂 Entrata in estrai_dati_da_pdf()")
    try:
        with fitz.open(percorso_pdf) as doc:
            testo = ""
            for pagina in doc:
                testo += pagina.get_text("text")

        logging.info(f"📏 Lunghezza testo PDF: {len(testo)}")
        logging.info(f"📄 Testo PDF estratto (prime 800c):\n{testo[:800]}")

        caratteristiche_azienda = {
            "forma_giuridica": estrai_valore(testo, r"Forma giuridica[:\s]+(.+?)\n"),
            "codice_ateco": estrai_valore(testo, r"Codice Ateco[:\s]+(.+?)\n"),
            "attivita_prevalente": estrai_valore(testo, r"Attività prevalente[:\s]+(.+?)\n")
        }

        bilancio = {
            # qui eventuali valori del bilancio se vuoi aggiungerli
        }

        return caratteristiche_azienda, bilancio

    except Exception as e:
        logging.error(f"❌ Errore apertura PDF: {e}")
        raise
