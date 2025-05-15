import logging
import openai
from indici_analisi import INDICI_REDDITIVITÀ, INDICI_SOLIDITÀ, INDICI_LIQUIDITÀ

import os
openai.api_key = os.getenv("OPENAI_API_KEY")

def analizza_completo_con_gpt(testo_bilancio):
    logging.info("\U0001f916 Avvio analisi GPT completa con struttura indici...")

    # Organizzazione degli indici in sezioni strutturate
    prompt = f"""
Sei un analista finanziario. Analizza il seguente testo di bilancio, estraendo e commentando gli indici chiave per ciascuna area:

**1. Redditività**
Indici da calcolare e interpretare:
- {chr(10).join(['- ' + indice for indice in INDICI_REDDITIVITÀ])}

**2. Solidità**
Indici da calcolare e interpretare:
- {chr(10).join(['- ' + indice for indice in INDICI_SOLIDITÀ])}

**3. Liquidità**
Indici da calcolare e interpretare:
- {chr(10).join(['- ' + indice for indice in INDICI_LIQUIDITÀ])}

Analizza il testo seguente ed elabora un report ordinato e comprensibile. Concludi con un giudizio sintetico sulla sostenibilità economico-finanziaria dell'azienda.

---
{testo_bilancio}
---
"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Sei un analista finanziario esperto di indici economico-finanziari."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4,
            max_tokens=2500
        )

        testo_output = response["choices"][0]["message"]["content"]
        logging.info("\U0001f4dc Report GPT generato correttamente.")
        return testo_output

    except Exception as e:
        logging.error(f"\u274c Errore durante la generazione del report GPT: {e}")
        return ""
