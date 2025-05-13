import logging
import os
import requests

from estrazione_pdf import estrai_testo_da_pdf
from gpt_module import analisi_completa_multipla
from claude_module import genera_relazione_con_claude
from matching_bandi import carica_bandi, filtra_bandi_compatibili

def esegui_analisi_completa(file_path, caratteristiche_impresa, csv_bandi_path):
    logging.info("🚀 Avvio esegui_analisi_completa")

    # 📄 Verifica esistenza file
    if not os.path.exists(file_path):
        logging.error(f"❌ File non trovato: {file_path}")
        return

    # 📄 Estrazione testo da PDF
    try:
        testo = estrai_testo_da_pdf(file_path)
        if not testo or len(testo.strip()) < 100:
            logging.error("❌ Testo PDF insufficiente o vuoto.")
            return
        logging.info("✅ Testo PDF estratto")
    except Exception as e:
        logging.error(f"❌ Errore estrazione testo da PDF: {e}")
        return

    # 🤖 Analisi GPT: se già esiste, riusa
    if os.path.exists("output_gpt.txt"):
        try:
            with open("output_gpt.txt", "r") as f:
                output_gpt = f.read()
            logging.info("📂 Caricato output GPT da file")
        except Exception as e:
            logging.error(f"❌ Errore lettura output_gpt.txt: {e}")
            return
    else:
        try:
            output_gpt = analisi_completa_multipla(testo)
            with open("output_gpt.txt", "w") as f:
                f.write(output_gpt)
            logging.info("✅ Analisi GPT completata e salvata")
        except Exception as e:
            logging.error(f"❌ Errore GPT: {e}")
            return

    # 🗂 Caricamento bandi
    try:
        bandi = carica_bandi(csv_bandi_path)
        if not bandi:
            logging.warning("⚠️ Nessun bando caricato dal CSV.")
            return
        logging.info(f"📥 {len(bandi)} bandi caricati")
    except Exception as e:
        logging.error(f"❌ Errore caricamento CSV bandi: {e}")
        return

    # 🎯 Filtro bandi compatibili
    try:
        bandi_compatibili = filtra_bandi_compatibili(bandi, caratteristiche_impresa)
        if not bandi_compatibili:
            logging.warning("⚠️ Nessun bando compatibile trovato.")
            return
        logging.info(f"✅ {len(bandi_compatibili)} bandi compatibili trovati")
    except Exception as e:
        logging.error(f"❌ Errore nel filtro bandi compatibili: {e}")
        return

    # 📄 Generazione relazione finale con Claude
    try:
        logging.info("📄 Generazione relazione conclusiva")
        relazione_finale = genera_relazione_con_claude(output_gpt, bandi_compatibili)

        if not relazione_finale or len(relazione_finale.strip()) < 100:
            logging.error("❌ Relazione finale vuota o troppo breve.")
            return

        with open("relazione_finale.txt", "w") as f:
            f.write(relazione_finale)
        logging.info("✅ Relazione finale salvata")

        # 📤 Invio via Make
        try:
            webhook_url = "https://hook.eu2.make.com/45pk0gb25uz3twjk3jzpu2eef8fg75w8"
            payload = {'relazione_finale': relazione_finale}
            response = requests.post(webhook_url, json=payload, timeout=10)

            if response.status_code == 200:
                logging.info("📨 Relazione inviata a Make")
            else:
                logging.error(f"❌ Errore invio Make: {response.status_code} - {response.text}")
        except Exception as e:
            logging.error(f"❌ Errore durante POST a Make: {e}")

    except Exception as e:
        logging.error(f"❌ Errore generazione relazione Claude: {e}")
        return
