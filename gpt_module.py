import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

MAX_TOKEN_GPT = 7000

# Funzione principale

def analisi_completa_multipla(testo):
    blocchi = dividi_blocchi(testo)
    risultati = []

    for i, blocco in enumerate(blocchi):
        path_blocco = f"blocco_{i+1}.txt"

        # Salta blocchi già analizzati
        if os.path.exists(path_blocco):
            try:
                with open(path_blocco, "r") as f:
                    risultati.append(f.read())
                continue
            except Exception as e:
                logging.error(f"Errore lettura {path_blocco}: {e}")
                continue

        # Analisi GPT
        try:
            risposta = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Sei un consulente esperto in finanza aziendale e strategia."},
                    {"role": "user", "content": blocco}
                ],
                max_tokens=MAX_TOKEN_GPT,
                temperature=0.7
            )
            testo_risposta = risposta.choices[0].message.content.strip()
            risultati.append(testo_risposta)

            with open(path_blocco, "w") as f:
                f.write(testo_risposta)
        except Exception as e:
            logging.error(f"Errore GPT sul blocco {i+1}: {e}")
            break

    return "\n\n".join(risultati)

# Funzione per dividere il testo (placeholder)
def dividi_blocchi(testo, max_caratteri=6000):
    parole = testo.split()
    blocchi = []
    blocco = []
    conta = 0

    for parola in parole:
        conta += len(parola) + 1
        if conta > max_caratteri:
            blocchi.append(" ".join(blocco))
            blocco = [parola]
            conta = len(parola) + 1
        else:
            blocco.append(parola)

    if blocco:
        blocchi.append(" ".join(blocco))

    return blocchi
