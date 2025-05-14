import openai
import logging

MAX_CARATTERI_GPT = 8000  # Limite per ciascun blocco, compatibile anche con Claude

def analisi_completa_multipla(testo):
    logging.info("🧠 Avvio analisi GPT multipla...")

    blocchi = []
    while len(testo) > MAX_CARATTERI_GPT:
        blocchi.append(testo[:MAX_CARATTERI_GPT])
        testo = testo[MAX_CARATTERI_GPT:]
    if testo:
        blocchi.append(testo)

    risultati = []
    totale = len(blocchi)

    for i, blocco in enumerate(blocchi):
        logging.info(f"🧠 GPT - Invio blocco {i+1} di {totale}")
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Sei un esperto analista finanziario."},
                    {"role": "user", "content": blocco}
                ],
                temperature=0.3,
                max_tokens=2000
            )
            risultato = response['choices'][0]['message']['content']
            risultati.append(risultato)
        except Exception as e:
            logging.error(f"Errore GPT nel blocco {i+1}: {e}")
            break

    logging.info("✅ Analisi GPT completata")
    return "\n\n".join(risultati)
