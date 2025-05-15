import logging
from estrazione_pdf import estrai_testo_da_pdf

def estrai_dati_da_pdf(file_path):
    try:
        logging.info("📣 Entrata in estrai_dati_da_pdf()")
        text = estrai_testo_da_pdf(file_path)  # ✅ Assegno il testo estratto
        logging.info(f"📏 Lunghezza testo PDF: {len(text)}")

        # (Esempio di logica su contenuto)
        if "Codice Fiscale" in text:
            logging.info("🔍 Codice Fiscale rilevato nel testo")
        else:
            logging.info("🚫 Codice Fiscale non presente")

        return text

    except Exception as e:
        logging.error(f"❌ Errore apertura PDF: {e}")
        logging.error(f"❌ Errore durante l'estrazione dati: {e}")
        return ""
