import os
import openai
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

def analisi_tecnica_gpt(testo):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Sei un analista finanziario esperto."},
            {"role": "user", "content": f"Analizza il seguente testo: {testo}"}
        ],
        temperature=0.5,
        max_tokens=800
    )
    return response.choices[0].message["content"]
