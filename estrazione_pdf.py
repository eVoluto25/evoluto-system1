import logging

def estrai_testo_da_pdf(file_path):
    try:
        logging.info("📂 Apertura file PDF in corso...")
        with open(file_path, "rb") as f:
            text = f.read().decode("utf-8", errors="ignore")
        logging.info(f"📏 Lunghezza testo PDF: {len(text)}")
        return text
    except Exception as e:
        logging.error(f"❌ Errore apertura PDF: {e}")
        logging.error(f"❌ Errore durante l'estrazione dati: {e}")
        return ""
