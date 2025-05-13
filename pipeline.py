import os
import logging
from estrazione_pdf import estrai_testo_da_pdf
from gpt_module import analisi_tecnica_gpt
from analisi_blocchi_gpt import analisi_completa_multipla
from claude_module import genera_relazione_con_claude
from matching_bandi import carica_bandi, filtra_bandi_compatibili

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
            with open("output_gpt.txt", "r") as f:
                output_gpt = f.read()
        except Exception as e:
            logging.error(f"Errore durante la lettura di output_gpt.txt: {e}")
            return
    else:
        logging.info("🧠 Avvio analisi GPT")
        try:
            output_gpt = analisi_completa_multipla(testo)
            logging.info("✅ Analisi GPT completata")
        except Exception as e:
            logging.error(f"Errore durante analisi_completa_multipla: {e}")
            return

        try:
            with open("output_gpt.txt", "w") as f:
                f.write(output_gpt)
            logging.info("💾 Analisi GPT salvata su file")
        except Exception as e:
            logging.error(f"Errore durante il salvataggio di output_gpt.txt: {e}")
            return

    try:
        logging.info("📥 Caricamento bandi")
        bandi = carica_bandi(csv_bandi_path)
        logging.info(f"✅ {len(bandi)} bandi caricati")
    except Exception as e:
        logging.error(f"Errore nel caricamento dei bandi: {e}")
        return

    try:
        logging.info("🔍 Filtro bandi compatibili")
        bandi_compatibili = filtra_bandi_compatibili(bandi, caratteristiche_impresa)
        logging.info(f"✅ Trovati {len(bandi_compatibili)} bandi compatibili")
    except Exception as e:
        logging.error(f"Errore nel filtraggio dei bandi: {e}")
        return

    try:
        logging.info("📄 Generazione relazione conclusiva")
        genera_relazione_con_claude(output_gpt, caratteristiche_impresa, bandi_compatibili)
        logging.info("✅ Relazione generata con successo")
    except Exception as e:
        logging.error(f"Errore durante la generazione della relazione: {e}")
        return
