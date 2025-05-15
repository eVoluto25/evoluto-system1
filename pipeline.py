import logging
from extractor import estrai_dati_da_pdf
from gpt_module import analizza_completo_con_gpt
from claude_module import genera_relazione_con_claude
from bandi_matcher import trova_bandi_compatibili
from aggiorna_bandi import aggiorna_bandi

def esegui_analisi_completa(percorso_pdf, email_destinatario):
    logging.info("🚀 Avvio pipeline: Estrazione → GPT → Bandi → Claude")

    try:
        logging.info("📄 Estrazione dati aziendali da PDF")
        caratteristiche_azienda, bilancio = estrai_dati_da_pdf(percorso_pdf)
        # Analisi GPT del bilancio
        analisi_finanziaria = analizza_completo_con_gpt(bilancio)
        logging.info(f"📊 Analisi GPT completata")

        # Ricerca bandi compatibili
        bandi_compatibili = trova_bandi_compatibili(caratteristiche_azienda, bilancio)
        logging.info(f"🎯 Bandi compatibili trovati: {len(bandi_compatibili)}")

        # Generazione relazione finale con Claude
        relazione_html = genera_relazione_con_claude(
            caratteristiche_azienda,
            bilancio,
            analisi_finanziaria,
            bandi_compatibili,
            email_destinatario
        )
        logging.info("📄 Relazione finale generata e inviata con successo")
        
        logging.info(f"📌 Caratteristiche: {caratteristiche_azienda}")
        logging.info(f"📊 Bilancio: {bilancio}")
    except Exception as e:
        logging.error(f"❌ Errore durante l'estrazione: {e}")
        return {"esito": "errore", "fase": "estrazione", "dettaglio": str(e)}

    try:
        logging.info("🌐 Aggiornamento bandi automatico in corso")
        aggiorna_bandi()
        logging.info("✅ Bandi aggiornati correttamente")
    except Exception as e:
        logging.warning(f"⚠️ Errore durante l’aggiornamento bandi: {e}")

    try:
        logging.info("🧠 Analisi GPT in corso")
        analisi_finanziaria = analizza_completo_con_gpt(bilancio)
        if not analisi_finanziaria:
            raise ValueError("Risposta GPT vuota")
        logging.info("✅ Analisi GPT completata")
    except Exception as e:
        logging.error(f"❌ Errore GPT: {e}")
        return {"esito": "errore", "fase": "gpt", "dettaglio": str(e)}

    try:
        logging.info("🎯 Matching bandi compatibili")
        bandi_trovati = trova_bandi_compatibili(caratteristiche_azienda, bilancio)
        logging.info(f"📑 Bandi trovati: {len(bandi_trovati)}")
    except Exception as e:
        logging.warning(f"⚠️ Errore matching bandi: {e}")
        bandi_trovati = []

    try:
        logging.info("🤖 Generazione relazione finale con Claude")
        relazione_finale = genera_relazione_con_claude(analisi_finanziaria, bandi_trovati)
        logging.info("✅ Relazione Claude generata correttamente")
    except Exception as e:
        logging.error(f"❌ Errore Claude: {e}")
        return {"esito": "errore", "fase": "claude", "dettaglio": str(e)}

    return {
        "esito": "ok",
        "email": email_destinatario,
        "caratteristiche_azienda": caratteristiche_azienda,
        "bilancio": bilancio,
        "analisi_gpt": analisi_finanziaria,
        "bandi_trovati": bandi_trovati,
        "relazione_claude": relazione_finale
    }
