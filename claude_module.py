import logging
import os
import anthropic
import json

# Inizializza il client Claude
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def genera_relazione_con_claude(output_gpt, bandi_compatibili):
    try:
        # Carica il prompt base
        with open("prompt_claude.txt", "r", encoding="utf-8") as f:
            prompt_base = f.read()

        # Prepara il testo dei bandi in formato leggibile
        testo_bandi = json.dumps(bandi_compatibili, indent=2, ensure_ascii=False)

        # Costruisce il prompt finale
        full_prompt = f"""{prompt_base}

-------------------
📊 ANALISI GPT:
{output_gpt}

-------------------
📌 BANDI COMPATIBILI:
{testo_bandi}
"""

        # Chiamata a Claude 3 con impostazioni ottimali
        risposta = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=2000,
            temperature=0.5,
            messages=[
                {
                    "role": "user",
                    "content": full_prompt
                }
            ]
        )

        logging.info("✅ Risposta Claude ricevuta")
        MAX_CARATTERI = 8000
    risposta_finale = risposta[:MAX_CARATTERI]
    return risposta_finale.content[0].text.strip()

    except Exception as e:
        logging.error(f"Errore durante la generazione relazione con Claude: {e}")
        return "Errore nella generazione della relazione con Claude."
