from claude_prompt_bandi import genera_paragrafo_bandi_claude
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

        logging.info("🧠 Avvio analisi GPT")
        output_gpt = analisi_completa_multipla(testo)
        logging.info("✅ Analisi GPT completata")

        logging.info("📥 Caricamento bandi")
        bandi = carica_bandi(csv_bandi_path)
        logging.info(f"✅ {len(bandi)} bandi caricati")

        logging.info("🔎 Filtro bandi compatibili")
        bandi_compatibili = filtra_bandi_compatibili(bandi, caratteristiche_impresa)
        logging.info(f"✅ Trovati {len(bandi_compatibili)} bandi compatibili")

        logging.info("📝 Generazione relazione finale con Claude")
        return genera_relazione_con_claude(output_gpt, "Preventivi", "Piano Ammortamento", bandi_compatibili)

    except Exception as e:
        logging.error(f"❌ Errore in esegui_analisi_completa: {e}")
        raise
