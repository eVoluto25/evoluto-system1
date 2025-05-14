import openai
import logging
from env_loader import carica_variabili_ambiente
from output_uploader import salva_output_html

def analizza_con_gpt(dati):
    config = carica_variabili_ambiente()
    openai.api_key = config["OPENAI_API_KEY"]

    logging.info(f"➡️ Bilancio ricevuto per GPT: {dati}")

    prompt = crea_prompt_gpt(dati)

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            temperature=0.3,
            max_tokens=1800,
            messages=[
                {"role": "system", "content": "Sei un esperto di analisi aziendale."},
                {"role": "user", "content": prompt}
            ]
        )

        contenuto = response['choices'][0]['message']['content']
        logging.info(f"✅ Output GPT ricevuto ({len(contenuto)} caratteri)")

        if not contenuto or contenuto.strip() == "":
            raise ValueError("❌ GPT ha restituito una risposta vuota")

        return contenuto

    except Exception as e:
        logging.error(f"❌ Errore durante la generazione GPT: {e}")
        return None

def crea_prompt_gpt(dati):
    return f"""Analizza i seguenti dati di bilancio dell'azienda:

- Ricavi: {dati.get('ricavi')}
- EBITDA: {dati.get('ebitda')}
- Utile netto: {dati.get('utile_netto')}
- Attivo totale: {dati.get('attivo_totale')}
- Patrimonio netto: {dati.get('patrimonio_netto')}

Commenta gli indici principali e segnala eventuali criticità.
"""  # chiusura f-string
