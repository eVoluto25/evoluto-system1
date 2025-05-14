import logging
from extractor import estrai_dati_da_pdf
from gpt_module import analizza_con_gpt
from matching_bandi import confronta_con_bandi
from claude_module import analizza_con_claude
from output_uploader import salva_output_html
from email_handler import invia_email
from bandi_updater import aggiorna_bandi
from env_loader import carica_variabili_ambiente
from monitor import registra_log

def esegui_pipeline(percorso_pdf, email_destinatario):
    logging.info("🚀 Inizio pipeline completa")

    try:
        logging.info("📥 Estrazione dati da visura PDF")
        caratteristiche_azienda, bilancio = estrai_dati_da_pdf(percorso_pdf)
    except Exception as e:
        logging.error(f"❌ Errore durante l'estrazione dati: {e}")
        return

    try:
        logging.info("🔄 Aggiornamento bandi pubblici")
        aggiorna_bandi()
    except Exception as e:
        logging.warning(f"⚠️ Impossibile aggiornare bandi: {e}")

    try:
        logging.info("🧠 Analisi GPT in corso...")
        analisi_finanziaria = analizza_con_gpt(bilancio)
    except Exception as e:
        logging.error(f"❌ Errore GPT: {e}")
        return

    try:
        logging.info("🔎 Matching tecnico bandi")
        bandi_compatibili = confronta_con_bandi(caratteristiche_azienda)
    except Exception as e:
        logging.error(f"❌ Errore matching bandi: {e}")
        return

    try:
        logging.info("🤖 Claude in esecuzione per analisi finale")
        risposta_claude = analizza_con_claude(caratteristiche_azienda, analisi_finanziaria, bandi_compatibili)
    except Exception as e:
        logging.error(f"❌ Claude fallito: {e}")
        return

    try:
        logging.info("💾 Salvataggio HTML GPT e Claude")
        url_html_gpt = salva_output_html("Analisi finanziaria GPT", analisi_finanziaria)
        url_html_claude = salva_output_html("Matching bandi Claude", risposta_claude)
    except Exception as e:
        logging.error(f"❌ Errore salvataggio output: {e}")
        return

    corpo_email = f"""Gentile imprenditore,

📊 Analisi finanziaria GPT:
{url_html_gpt}

🎯 Opportunità da bandi pubblici (Claude):
{url_html_claude}

Cordiali saluti,
Il team
"""  # chiusura corretta

    try:
        invia_email(email_destinatario, "Risultati Analisi Aziendale", corpo_email)
        logging.info("📤 Email inviata con successo")
    except Exception as e:
        logging.error(f"❌ Invio email fallito: {e}")

    try:
        registra_log({
            "email": email_destinatario,
            "gpt": url_html_gpt,
            "claude": url_html_claude,
            "status": "ok"
        })
        logging.info("🗂️ Log sessione salvato")
    except Exception as e:
        logging.error(f"❌ Log fallito: {e}")
