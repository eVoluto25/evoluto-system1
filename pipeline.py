import logging
import os

from estrazione_pdf import estrai_testo_da_pdf
from gpt_module import analisi_completa_multipla
from analisi_blocchi_gpt import analisi_completa_multipla
from claude_module import genera_relazione_con_claude
from matching_bandi import carica_bandi, filtra_bandi_compatibili
from email_handler import invia_email

def esegui_analisi_completa(file_path, caratteristiche_impresa, csv_bandi_path):
    logging.info("🚀 Avviata esegui_analisi_completa()")

    try:
        logging.info("📄 Estrazione testo PDF")
        testo = estrai_testo_da_pdf(file_path)
        logging.info("✅ Testo estratto")
    except Exception as e:
        logging.error(f"Errore durante l'estrazione del testo: {e}")
        return

    logging.info("🧠 Verifica salvataggio analisi GPT...")

    if os.path.exists("output_gpt.txt"):
        logging.info("📄 Analisi GPT già esistente, caricamento da file")
        try:
            from output_uploader import salva_output_html

    # Salvataggio HTML GPT
    url_html_gpt = salva_output_html("Analisi finanziaria GPT", output_gpt)

    # Claude HTML
    
                output_gpt = f.read()
        except Exception as e:
            logging.error(f"Errore durante la lettura di output_gpt.txt: {e}")
            return
    else:
        logging.info("🧠 Avvio analisi GPT")
        try:
            output_gpt = analisi_completa_multipla(testo)
            logging.info("✅ Analisi GPT completata")
            with open("output_gpt.txt", "w") as f:
                f.write(output_gpt)
        except Exception as e:
            logging.error(f"Errore durante analisi_completa_multipla: {e}")
            return

    logging.info("📥 Caricamento bandi")
    try:
        bandi = carica_bandi(csv_bandi_path)
        logging.info(f"✅ {len(bandi)} bandi caricati")
    except Exception as e:
        logging.error(f"Errore durante il caricamento dei bandi: {e}")
        return

    logging.info("🔍 Filtro bandi compatibili")
    try:
        bandi_compatibili = filtra_bandi_compatibili(bandi, caratteristiche_impresa)
        logging.info(f"✅ Trovati {len(bandi_compatibili)} bandi compatibili")
    except Exception as e:
        logging.error(f"Errore nel filtraggio dei bandi: {e}")
        return

    try:
        logging.info("🧾 Generazione relazione con Claude")
        relazione_finale = genera_relazione_con_claude(output_gpt, bandi_compatibili)

        # Salva relazione finale
        url_html_claude = salva_output_html("Matching bandi Claude", relazione_finale)
            f.write(relazione_finale)

        logging.info("✅ Relazione finale salvata")

        # ✅ Costruisci testo email limitato e con link GPT
        corpo_email = f"""Gentile cliente,

📊 Analisi finanziaria GPT:
{url_html_gpt}

🎯 Opportunità e bandi compatibili (Claude):
{url_html_claude}"""

        # ✅ Log email
        with open("log_email.txt", "w", encoding="utf-8") as f:
            f.write(f"Destinatario: info@capitaleaziendale.it\nOggetto: Relazione Claude\n\n{corpo_email.strip()}")

        logging.info("📤 Log email salvato")

        # ✅ Invio tramite Make
        import requests
        requests.post(
            "https://hook.eu2.make.com/WEBHOOK_CLAUDE",  # sostituisci con il tuo webhook attivo
            json={
                "subject": "📈 Relazione strategica conclusa",
                "body": corpo_email
            }
        )

        logging.info("📩 Email inviata via Make")
        relazione_finale = genera_relazione_con_claude(output_gpt, bandi_compatibili)
        url_html_claude = salva_output_html("Matching bandi Claude", relazione_finale)
            f.write(relazione_finale)
        logging.info("✅ Relazione finale salvata")

        # 🔽 Tracciamento email inviata
        log_email = f"Destinatario: info@capitaleaziendale.it\nOggetto: Nuova relazione strategica generata da Claude\n\n{relazione_finale}"
        with open("log_email.txt", "w", encoding="utf-8") as f:
            f.write(log_email.strip())

        logging.info("📤 Log email salvato")

        # Invia la relazione via email al gestore
        invia_email(
            destinatario="info@capitaleaziendale.it",
            oggetto="Nuova relazione strategica generata da Claude",
            corpo=relazione_finale
        )
        logging.info("📩 Relazione inviata a info@capitaleaziendale.it")

    except Exception as e:
        logging.error(f"Errore durante la generazione o invio della relazione finale: {e}")
        return
