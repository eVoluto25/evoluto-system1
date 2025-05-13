import openai
import tiktoken
import logging
import os
import time

openai.api_key = os.getenv("OPENAI_API_KEY")

def conta_token(testo, model="gpt-3.5-turbo"):
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(testo))

def dividi_in_blocchi(testo, max_token=10000, model="gpt-3.5-turbo"):
    encoding = tiktoken.encoding_for_model(model)
    tokens = encoding.encode(testo)
    blocchi = []
    for i in range(0, len(tokens), max_token):
        blocco_token = tokens[i:i+max_token]
        blocchi.append(encoding.decode(blocco_token))
    return blocchi

def analizza_blocco(blocco_testo, numero, totale):
    prompt = f"""
Questa è la parte {numero} di {totale} del bilancio aziendale. Analizza solo questa sezione e concentrati su:
- andamento economico e finanziario
- segnali di rischio
- indicatori di solidità o debolezza
Attendi le altre parti per l’analisi complessiva.
"""
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Sei un analista finanziario esperto."},
            {"role": "user", "content": prompt + "\n\n" + blocco_testo}
        ],
        temperature=0.3,
        max_tokens=1500
    )
    return response.choices[0].message["content"]

def sintetizza_blocchi(analisi_blocchi):
    joined_text = "\n\n".join(analisi_blocchi)
    prompt_finale = """
Hai ricevuto l’analisi delle sezioni di un bilancio aziendale. Ora uniscile in una relazione unica che:
- riassuma i punti salienti
- evidenzi criticità, margini, solidità o squilibri
- suggerisca 3 azioni strategiche per migliorare la gestione.
"""
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Sei un analista finanziario professionale."},
            {"role": "user", "content": prompt_finale + "\n\n" + joined_text}
        ],
        temperature=0.3,
        max_tokens=2000
    )
    return response.choices[0].message["content"]

def analisi_completa_multipla(testo_lungo):
    logging.info("🚀 Avvio segmentazione e analisi GPT")
    blocchi = dividi_in_blocchi(testo_lungo)
    logging.info(f"📦 Diviso in {len(blocchi)} blocchi")

    analisi_blocchi = []
    for i, blocco in enumerate(blocchi):
        logging.info(f"🔍 Analisi blocco {i+1}/{len(blocchi)}")
        output = analizza_blocco(blocco, i+1, len(blocchi))
        analisi_blocchi.append(output)
        time.sleep(2)  # Delay di sicurezza per evitare il rate limit

    logging.info("🧠 Sintesi finale in corso...")
    sintesi = sintetizza_blocchi(analisi_blocchi)
    return sintesi
