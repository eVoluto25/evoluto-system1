import os
import logging
import openai
from output_uploader import salva_output_html
from env_loader import carica_variabili_ambiente

def analizza_con_gpt(dati):
    logging.info("🧠 [GPT] Inizio analisi GPT-3.5")

    config = carica_variabili_ambiente()
    openai.api_key = config["OPENAI_API_KEY"]

    prompt = crea_prompt_gpt(dati)

    logging.info("👉 [GPT] Prompt inviato a GPT:")
    logging.info(prompt)

    try:
        risposta = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            temperature=0.3,
            max_tokens=1800,
            messages=[
                {"role": "system", "content": "Sei un CFO esperto in analisi di bilancio. Analizza solidità, sostenibilità e redditività aziendale."},
                {"role": "user", "content": prompt}
            ]
        )

        logging.info("✅ [GPT] Risposta API ricevuta:")
        logging.info(str(risposta))

        contenuto = risposta['choices'][0]['message']['content']

        if not contenuto or contenuto.strip() == "":
            raise ValueError("GPT ha restituito una risposta vuota.")

        url_html = salva_output_html("Analisi_finanziaria_GPT", contenuto)
        logging.info(f"✅ [GPT] Report HTML salvato: {url_html}")
        return url_html

    except Exception as e:
        logging.error(f"❌ [GPT] Errore durante la generazione GPT: {e}")
        return None

def crea_prompt_gpt(dati):
    return f"""Analizza i seguenti dati di bilancio (ultimi disponibili):

Dati economici:
- Ricavi: {dati.get('ricavi')}
- Utile netto: {dati.get('utile_netto')}
- EBITDA: {dati.get('ebitda')}
- Attivo totale: {dati.get('attivo_totale')}
- Patrimonio netto: {dati.get('patrimonio_netto')}
- Debiti finanziari: {dati.get('debiti_finanziari')}
- Oneri finanziari: {dati.get('oneri_finanziari')}
- Debiti verso fornitori: {dati.get('debiti_fornitori')}
- Rimanenze: {dati.get('rimanenze')}
- Liquidità: {dati.get('liquidita')}
- Ammortamenti: {dati.get('ammortamenti')}
- Flusso di cassa operativo: {dati.get('cfo')}
- Rata annua prevista (eventuale prestito): {dati.get('rata_annua')}

Calcola e commenta:
- ROE
- ROI
- ROS
- DSCR
- Current Ratio
- Equity Ratio
- Incidenza oneri finanziari
- Copertura investimenti
- Incidenza rimanenze
- Copertura debiti fornitori

Fornisci una relazione chiara, utile all’imprenditore per capire la salute finanziaria aziendale."""
