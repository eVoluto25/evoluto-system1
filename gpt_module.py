import os
from dotenv import load_dotenv
import openai

# Costante per limitare la dimensione del testo (in byte, circa 20.000 caratteri)
MAX_GPT_OUTPUT_LENGTH = 20000

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def genera_analisi(bilancio, visura):
    try:
        prompt = f"""
Sei un analista finanziario esperto. Analizza i seguenti dati aziendali (bilancio + visura camerale) per identificare punti di forza, criticità economiche, patrimoniali e gestionali.
L'obiettivo è ottenere un quadro sintetico ma chiaro della situazione, utile per valutare la compatibilità con strumenti di finanza agevolata.

⚠️ IMPORTANTE: la tua risposta verrà poi elaborata da un secondo sistema con forti limiti di spazio (max 9 MB).
⛔ Non superare 20.000 caratteri.
✅ Sii concreto, focalizzato e sintetico.

--- DATI AZIENDALI ---
BILANCIO:
{bilancio}

VISURA CAMERALE:
{visura}

"""

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=3000,
            temperature=0.4,
        )

        risultato = response['choices'][0]['message']['content'].strip()

        # Limitazione esplicita della lunghezza per compatibilità Claude
        if len(risultato.encode("utf-8")) > MAX_GPT_OUTPUT_LENGTH:
            risultato = risultato[:MAX_GPT_OUTPUT_LENGTH]

        return risultato

    except Exception as e:
        print("Errore durante la generazione dell'analisi GPT:", e)
        return "Errore durante l'elaborazione dell'analisi GPT."
