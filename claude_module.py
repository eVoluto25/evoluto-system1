import os
from dotenv import load_dotenv
import anthropic

# Costanti
MAX_CARATTERI = 9000

# Carica variabili ambiente
load_dotenv()

# Inizializza client Claude
client = anthropic.Anthropic(api_key=os.getenv("CLAUDE_API_KEY"))

def genera_relazione_con_claude(output_gpt, bandi_compatibili):
    try:
        # Costruzione prompt direttamente qui, senza dipendere da altri file
        prompt = f"""
🧠 ANALISI GPT:
{output_gpt}

📌 BANDI COMPATIBILI:
{bandi_compatibili}
"""

        logging.info("📰 Prompt Claude:\n" + prompt)

        risposta = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=MAX_CARATTERI,
            temperature=0.6,
            system="Sei un CFO esperto in analisi aziendale, merito creditizio e strategia. Ricevi l'output GPT e l'elenco dei bandi compatibili. Fornisci da 1 a 10 soluzioni reali, concrete, chiare e sintetiche per migliorare l'impresa.",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        logging.info("✅ Claude ha restituito la relazione.")
        risposta_finale = risposta.content[0].text[:MAX_CARATTERI]
        return risposta_finale

    except Exception as e:
        logging.error(f"Errore durante la generazione della relazione con Claude: {e}")
        return "Errore durante la generazione della relazione"
