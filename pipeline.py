import logging
from analisi_blocchi_gpt import genera_analisi_gpt
from analisi_claude import genera_relazione_con_claude
from estrattore_pdf import estrai_testo_da_pdf
from email_handler import invia_email
from output_uploader import salva_output_html

def esegui_analisi_completa(percorso_pdf, destinatario_email):
    logging.info("📥 Inizio analisi per: " + percorso_pdf)

    try:
        dati_estratti = estrai_testo_da_pdf(percorso_pdf)
        logging.info("✅ Testo estratto dalla visura")
    except Exception as e:
        logging.error(f"❌ Errore estrazione PDF: {e}")
        return

    try:
        output_gpt = genera_analisi_gpt(dati_estratti)
        logging.info("✅ Analisi GPT completata")
    except Exception as e:
        logging.error(f"❌ Errore generazione GPT: {e}")
        return

    try:
        relazione_finale = genera_relazione_con_claude(dati_estratti, output_gpt)
        logging.info("✅ Relazione Claude completata")
    except Exception as e:
        logging.error(f"❌ Errore Claude: {e}")
        return

    try:
        url_html_gpt = salva_output_html("Analisi finanziaria GPT", output_gpt)
    except Exception as e:
        logging.error(f"❌ Errore salvataggio HTML GPT: {e}")
        return

    try:
        url_html_claude = salva_output_html("Matching bandi Claude", relazione_finale)
    except Exception as e:
        logging.error(f"❌ Errore salvataggio HTML Claude: {e}")
        return

    corpo_email = f"""Gentile cliente,

📊 Analisi finanziaria GPT:
{url_html_gpt}

🎯 Opportunità e bandi compatibili (Claude):
{url_html_claude}

Cordiali saluti,  
Il team eVoluto
"""

    try:
        invia_email(destinatario_email, "Esito Verifica Aziendale", corpo_email)
        logging.info("📤 Email inviata con successo")
    except Exception as e:
        logging.error(f"❌ Errore invio email: {e}")
