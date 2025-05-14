import os
from dotenv import load_dotenv
from prompt_loader import prompt_claude
import anthropic
import logging

# Costanti
MAX_CARATTERI = 9000

# Carica variabili ambiente
load_dotenv()

# Inizializza client Claude
client = anthropic.Anthropic(api_key=os.getenv("CLAUDE_API_KEY"))

def genera_relazione_con_claude(bilancio, visura, bandi):
    try:
        prompt = prompt_claude(bilancio, visura, bandi)

        # Log invio prompt
        logging.info("📨 Prompt Claude:\n" + prompt)

        # Chiamata a Claude
        risposta = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=MAX_CARATTERI,
            temperature=0.6,
            system="Sei un CFO esperto in analisi aziendale, merito creditizio e strategia. Ricevi l'output GPT e l'elenco dei bandi compatibili.",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        # Log esito Claude
        logging.info("✅ Claude ha restituito la relazione.")

        risposta_finale = risposta.content[0].text[:MAX_CARATTERI]
        return risposta_finale

    except Exception as e:
        logging.error(f"❌ Errore durante la generazione della relazione con Claude: {e}")
        return "Errore durante la generazione della relazione"
