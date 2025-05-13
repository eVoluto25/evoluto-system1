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
cartella_blocchi = "blocchi_salvati"

if os.path.exists("output_gpt.txt"):
    logging.info("📄 Analisi GPT già esistente, caricamento da file")
    try:
        with open("output_gpt.txt", "r") as f:
            output_gpt = f.read()
    except Exception as e:
        logging.error(f"Errore durante la lettura di output_gpt.txt: {e}")
        return

elif os.path.exists(cartella_blocchi):
    blocchi = sorted([f for f in os.listdir(cartella_blocchi) if f.startswith("blocco_")])
    if blocchi:
        logging.info("📦 Ricompongo output_gpt.txt dai blocchi salvati")
        try:
            contenuti = []
            for file in blocchi:
                with open(os.path.join(cartella_blocchi, file), "r", encoding="utf-8") as f:
                    contenuti.append(f.read())
            output_gpt = "\n\n".join(contenuti)
            with open("output_gpt.txt", "w") as f:
                f.write(output_gpt)
        except Exception as e:
            logging.error(f"Errore durante la ricostruzione da blocchi: {e}")
            return
    else:
        logging.warning("⚠️ Nessun blocco trovato nella cartella, avvio GPT")
        try:
            logging.info("🧠 Avvio analisi GPT")
            output_gpt = analisi_completa_multipla(testo)
            logging.info("✅ Analisi GPT completata")
            with open("output_gpt.txt", "w") as f:
                f.write(output_gpt)
        except Exception as e:
            logging.error(f"Errore durante analisi_completa_multipla: {e}")
            return

else:
    logging.warning("📂 Cartella blocchi non trovata, avvio GPT")
    try:
        logging.info("🧠 Avvio analisi GPT")
        output_gpt = analisi_completa_multipla(testo)
        logging.info("✅ Analisi GPT completata")
        with open("output_gpt.txt", "w") as f:
            f.write(output_gpt)
    except Exception as e:
        logging.error(f"Errore durante analisi_completa_multipla: {e}")
        return
