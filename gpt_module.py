import os
from dotenv import load_dotenv
import openai
import logging

load_dotenv()

# Imposta la chiave API
openai.api_key = os.getenv("OPENAI_API_KEY")

# Costanti di controllo dimensione massima
MAX_CARATTERI_GPT = 12000  # Limite prudenziale

# Funzione per analisi GPT su un blocco

def analisi_completa_multipla(testo):
    blocchi = []
    testo_corrente = ""

    for paragrafo in testo.split("\n"):
        if len(testo_corrente) + len(paragrafo) < MAX_CARATTERI_GPT:
            testo_corrente += paragrafo + "\n"
        else:
            blocchi.append(testo_corrente)
            testo_corrente = paragrafo + "\n"

    if testo_corrente:
        blocchi.append(testo_corrente)

    risultati = []

    for i, blocco in enumerate(blocchi):
        try:
            logging.info(f"🧠 GPT - Invio blocco {i+1} di {len(blocchi)}")
            risposta = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Sei un esperto di analisi economico-finanziaria. Analizza il seguente testo estratto da una visura e un bilancio."},
                    {"role": "user", "content": blocco}
                ]
            )
            risultato = risposta.choices[0].message.content.strip()
            risultati.append(risultato)
        except Exception as e:
            logging.error(f"Errore nel blocco {i+1}: {e}")
            break

    return "\n\n".join(risultati)
