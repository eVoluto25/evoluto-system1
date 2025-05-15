import logging
from estrazione_pdf import estrai_testo_da_pdf

def estrai_dati_da_pdf(percorso_pdf):
    try:
        logging.info("📩 Entrata in estrai_dati_da_pdf()")
        text = estrai_testo_da_pdf(percorso_pdf)
        logging.info(f"📏 Lunghezza testo PDF: {len(text)}")

        caratteristiche = {}
        bilancio = {}

        # Esempio semplice: verifica presenza di parole chiave nel testo PDF
        if "Codice Fiscale" in text:
            caratteristiche["codice_fiscale"] = "Rilevato"
        else:
            caratteristiche["codice_fiscale"] = "Non presente"

        if "Capitale Sociale" in text:
            bilancio["capitale_sociale"] = "Presente"
        else:
            bilancio["capitale_sociale"] = "Non presente"

        return caratteristiche, bilancio

    except Exception as e:
        logging.error(f"❌ Errore apertura PDF: {e}")
        logging.error(f"❌ Errore durante l'estrazione dati: {e}")
        return {}, {}
