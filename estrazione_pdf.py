import logging

def estrai_testo_da_pdf(file_path):
    try:
        logging.info("📥 Apertura file PDF per estrazione testo")
        with open(file_path, "rb") as f:
            contenuto = f.read().decode("utf-8", errors="ignore")
            logging.info(f"📏 Lunghezza testo PDF estratto: {len(contenuto)} caratteri")
            return contenuto
    except Exception as e:
        logging.error(f"❌ Errore in estrai_testo_da_pdf: {e}")
        return ""
