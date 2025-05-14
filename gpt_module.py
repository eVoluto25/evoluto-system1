
import os
from openai import openai
from dotenv import load_dotenv

load_dotenv()
client = openai(api_key=os.getenv("OPENAI_API_KEY"))

def analisi_completa_multipla(testo):
    blocchi = dividi_blocchi(testo)
    risultati = []

    for i, blocco in enumerate(blocchi):
        path_blocco = f"blocco_{i+1}.txt"

        if os.path.exists(path_blocco):
            with open(path_blocco, "r") as f:
                risultati.append(f.read())
            continue

        try:
            risposta = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": blocco}],
                temperature=0.6
            )
            risultati.append(risposta.choices[0].message.content)
            with open(path_blocco, "w") as f:
                f.write(risposta.choices[0].message.content)
        except Exception as e:
            print(f"Errore nel blocco {i+1}:", e)
            break

    return "\n\n".join(risultati)

# Alias per retrocompatibilità
analisi_tecnica_gpt = analisi_completa_multipla
