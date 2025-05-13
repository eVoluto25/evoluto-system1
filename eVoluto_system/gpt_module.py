import os
from openai import openai
from dotenv import load_dotenv
from prompt_loader import prompt_gpt

# Carica il file .env
load_dotenv()

# Inizializza il client OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analisi_tecnica_gpt(bilancio, visura, bandi):
    try:
        prompt = prompt_gpt(bilancio, visura, bandi)

        response = openai.chat.completions.create(
            model="gpt-3.5 turbo",
            messages=[
                {"role": "system", "content": "Sei un CFO esperto in analisi aziendale, merito creditizio e strategia."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=1500
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print("Errore durante l'elaborazione GPT:", e)
        return "Errore durante l'elaborazione GPT"
