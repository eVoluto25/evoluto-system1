import logging
from extractor import estrai_dati_da_pdf
from gpt_module import analizza_completo_con_gpt
from claude_module import genera_relazione_con_claude
from bandi_matcher import trova_bandi_compatibili
from bandi_utils import formatta_bandi

def esegui_analisi_completa(percorso_pdf, email_destinatario):
    try:
        logging.info("📥 Avvio esecuzione analisi completa")

        # Estrazione dati dal PDF
        caratteristiche_azienda, bilancio = estrai_dati_da_pdf(percorso_pdf)
        logging.info("📄 Estrazione PDF completata")

        # Analisi GPT a blocchi
        analisi_finanziaria = analizza_blocchi_gpt(bilancio)
        if not analisi_finanziaria:
            logging.error("❌ GPT ha fallito – Claude non verrà chiamato.")
            return {"esito": "errore", "fase": "gpt", "dettaglio": "Nessuna risposta utile da GPT"}

        # Match bandi
        bandi_compatibili = trova_bandi_compatibili(caratteristiche_azienda, bilancio)
        if not bandi_compatibili:
            logging.warning("⚠️ Nessun bando compatibile – Claude non verrà chiamato.")
            return {"esito": "errore", "fase": "matching", "dettaglio": "Nessun bando individuato"}

        # Generazione relazione con Claude
        relazione_html = genera_relazione_con_claude(
            caratteristiche_azienda,
            bilancio,
            analisi_finanziaria,
            bandi_compatibili,
            email_destinatario
        )

        logging.info("📤 Relazione HTML generata e inviata con successo.")
        return {"esito": "ok"}

    except Exception as e:
        logging.exception(f"🔥 Errore generico nella pipeline: {e}")
        return {"esito": "errore", "fase": "generale", "dettaglio": str(e)}

    try:
        logging.info("🌐 Aggiornamento bandi automatico in corso")
        aggiorna_bandi()
        logging.info("✅ Bandi aggiornati correttamente")
    except Exception as e:
        logging.warning(f"⚠️ Errore durante l’aggiornamento bandi: {e}")

    try:
        logging.info("🧠 Analisi GPT in corso")
        analisi_finanziaria = analizza_completo_con_gpt(bilancio, caratteristiche_azienda)
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
