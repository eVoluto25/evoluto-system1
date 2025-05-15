import logging
from extractor import estrai_dati_da_pdf
from gpt_module import analizza_completo_con_gpt
from claude_module import genera_relazione_con_claude
from bandi_matcher import trova_bandi_compatibili
from email_handler import recupera_email_con_allegati


def esegui_analisi_completa(percorso_pdf, email_destinatario):
    logging.info("📥 File ricevuto via API: %s, email: %s", percorso_pdf, email_destinatario)

    try:
        logging.info("🚀 Inizio pipeline completa")

        logging.info("📄 Estrazione dati da visura PDF")
        caratteristiche_azienda, bilancio = estrai_dati_da_pdf(percorso_pdf)
        logging.info(f"📎 Lunghezza testo PDF: {len(bilancio)}")

    except Exception as e:
        logging.error(f"❌ Errore apertura PDF: {e}")
        logging.error(f"❌ Errore durante l'estrazione dati: {e}")
        return

    try:
        logging.info("🌐 Aggiornamento bandi pubblici")
        from aggiorna_bandi import aggiorna_bandi
        aggiorna_bandi()
    except Exception as e:
        logging.warning(f"⚠️ Impossibile aggiornare bandi: {e}")

    try:
        logging.info("🎯 Chiamata a GPT in corso...")
        analisi_finanziaria = analizza_completo_con_gpt(bilancio)
        if not analisi_finanziaria or analisi_finanziaria.strip() == "":
            logging.error("❌ GPT ha restituito una risposta vuota o nulla.")
            return
    except Exception as e:
        logging.error(f"❌ Errore durante analisi GPT: {e}")
        return

    try:
        logging.info("🤖 Matching bandi compatibili")
        bandi_trovati = trova_bandi_compatibili(caratteristiche_azienda, bilancio)
    except Exception as e:
        logging.warning(f"⚠️ Errore durante il matching bandi: {e}")
        bandi_trovati = []

    try:
        logging.info("🧠 Generazione relazione finale con Claude")
        relazione_finale = genera_relazione_con_claude(analisi_finanziaria, bandi_trovati)
    except Exception as e:
        logging.error(f"❌ Errore generazione relazione Claude: {e}")
        return

    try:
        logging.info("📤 Invio email al destinatario")
        from email_sender import invia_email_con_risultati
        invia_email_con_risultati(email_destinatario, relazione_finale)
    except Exception as e:
        logging.error(f"❌ Errore invio email: {e}")


def start_da_email():
    logging.info("📬 Avvio lettura email in arrivo")
    email, file_path = recupera_email_con_allegati()
    if email and file_path:
        esegui_analisi_completa(file_path, email)


if __name__ == "__main__":
    import sys
    if len(sys.argv) == 3:
        esegui_analisi_completa(sys.argv[1], sys.argv[2])
    else:
        start_da_email()
