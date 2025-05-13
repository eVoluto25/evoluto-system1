import logging
import time
import os
from gpt_module import analisi_tecnica_gpt

# Suddivide il testo in blocchi da massimo 10000 caratteri
def suddividi_in_blocchi(testo, dimensione_blocco=10000):
    parole = testo.split()
    blocchi = []
    blocco_corrente = []
    caratteri_correnti = 0

    for parola in parole:
        if caratteri_correnti + len(parola) + 1 <= dimensione_blocco:
            blocco_corrente.append(parola)
            caratteri_correnti += len(parola) + 1
        else:
            blocchi.append(" ".join(blocco_corrente))
            blocco_corrente = [parola]
            caratteri_correnti = len(parola) + 1

    if blocco_corrente:
        blocchi.append(" ".join(blocco_corrente))

    return blocchi

# Analisi GPT su tutti i blocchi

def analisi_completa_multipla(testo):
    blocchi = suddividi_in_blocchi(testo)
    logging.info(f"📦 Diviso in {len(blocchi)} blocchi")

    risultati = []
    cartella_blocchi = "blocchi_salvati"
    os.makedirs(cartella_blocchi, exist_ok=True)

    for i, blocco in enumerate(blocchi):
        nome_file = os.path.join(cartella_blocchi, f"blocco_{i+1}.txt")

        if os.path.exists(nome_file):
            logging.info(f"🔁 Blocco {i+1}/{len(blocchi)} già elaborato, salto.")
            with open(nome_file, "r", encoding="utf-8") as f:
                risultati.append(f.read())
            continue

        try:
            logging.info(f"🧠 Analisi blocco {i+1}/{len(blocchi)}")
            risposta = analisi_tecnica_gpt(blocco)
            risultati.append(risposta)
            with open(nome_file, "w", encoding="utf-8") as f:
                f.write(risposta)
            time.sleep(2)  # Delay di sicurezza per evitare il rate limit
        except Exception as e:
            logging.error(f"❌ Errore nel blocco {i+1}: {e}")
            break

    return "\n\n".join(risultati)

# Sintesi finale (opzionale per ridurre tokens)
def sintetizza_blocchi(analisi_blocchi):
    # Da usare se vuoi fare sintesi dopo i blocchi
    pass
