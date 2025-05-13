# gpt_module.py
from openai import openai
import os

client = openai(api_key=os.getenv("OPENAI_API_KEY"))

def analisi_tecnica_gpt(testo):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "Sei un analista finanziario esperto. Analizza il testo e fornisci insight tecnici."
            },
            {
                "role": "user",
                "content": testo
            }
        ],
        temperature=0.3,
        max_tokens=1500
    )
    return response.choices[0].message.content

def analisi_completa_multipla(testo):
    import os, time
    from analisi_blocchi_gpt import dividi_blocchi

    blocchi = dividi_blocchi(testo)
    risposte = []

    for i, blocco in enumerate(blocchi):
        print(f"\n\033[94mAnalisi blocco {i+1}/{len(blocchi)}\033[0m")
        risposta = analisi_tecnica_gpt(blocco)
        risposte.append(risposta)

        # Salva il blocco in un file singolo per ogni passo
        with open(f"blocco_{i+1}.txt", "w") as f:
            f.write(risposta)
        time.sleep(2)  # Delay per evitare rate limit

    return "\n\n".join(risposte)
