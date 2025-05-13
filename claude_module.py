import os
from dotenv import load_dotenv
import anthropic

# Costanti
MAX_CARATTERI = 9000

# Carica variabili ambiente
load_dotenv()

# Inizializza client Claude
client = anthropic.Anthropic(api_key=os.getenv("CLAUDE_API_KEY"))

def genera_relazione_con_claude(bilancio, visura, bandi):
    try:
        prompt = f"""
OUTPUT GPT:
{bilancio}

VISURA CAMERALE:
{visura}

BANDI COMPATIBILI:
{bandi}
"""

        risposta = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=MAX_CARATTERI,
            temperature=0.6,
            system="Sei un CFO esperto in analisi aziendale, merito creditizio e strategia. Ricevi l'output GPT e l'elenco dei bandi compatibili per l'azienda. Sulla base di queste informazioni, fornisci da 1 a 10 soluzioni reali, concrete, chiare e sintetiche per migliorare l'impresa. Evita premesse inutili.",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        risposta_finale = risposta.content[0].text[:MAX_CARATTERI]
        return risposta_finale

    except Exception as e:
        print("Errore durante la generazione della relazione con Claude:", e)
        return "Errore durante la generazione della relazione"
