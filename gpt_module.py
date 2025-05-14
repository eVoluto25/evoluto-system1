import os
import openai
from dotenv import load_dotenv
import logging

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def dividi_blocchi(testo, max_caratteri=3000):
    parole = testo.split()
    blocchi, blocco_corrente = [], []
    lunghezza_corrente = 0

    for parola in parole:
        if lunghezza_corrente + len(parola) + 1 <= max_caratteri:
            blocco_corrente.append(parola)
            lunghezza_corrente += len(parola) + 1
        else:
            blocchi.append(" ".join(blocco_corrente))
            blocco_corrente = [parola]
            lunghezza_corrente = len(parola) + 1

    if blocco_corrente:
        blocchi.append(" ".join(blocco_corrente))

    return blocchi

def analisi_completa_multipla(testo):
    blocchi = dividi_blocchi(testo)
    risultati = []

    for i, blocco in enumerate(blocchi):
        logging.info(f"\U0001f9e0 GPT - Invio blocco {i+1} di {len(blocchi)}")
        try:
            risposta = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": blocco}
                ]
            )
            risultati.append(risposta.choices[0].message.content)
        except Exception as e:
            logging.error(f"Errore nel blocco {i+1}: {e}")
            break

    return "\n\n".join(risultati)
