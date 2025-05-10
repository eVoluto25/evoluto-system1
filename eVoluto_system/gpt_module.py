import os
from openai import OpenAI
from dotenv import load_dotenv
from prompt_loader import prompt_gpt

# Carica il file .env
load_dotenv()

# Inizializza il client OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analisi_tecnica_gpt(bilancio, visura, bandi):
    try:
        prompt = prompt_gpt(bilancio, visura, bandi)

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Sei un CFO esperto in analisi aziendale, merito creditizio e strategia."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print("Errore durante l'elaborazione GPT:", e)
        return "Errore durante l'elaborazione GPT"