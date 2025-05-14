import os
from dotenv import load_dotenv
import anthropic

# Costanti
MAX_CARATTERI = 9500

# Carica variabili ambiente
load_dotenv()

# Inizializza client Claude
client = anthropic.Anthropic(api_key=os.getenv("CLAUDE_API_KEY"))

def genera_relazione_con_claude(analisi_gpt, visura, bandi_compatibili):
    try:
        print("🟡 Inizio generazione relazione con Claude...")

        # Estrae solo i titoli dei bandi
        titoli_bandi = [bando.get("titolo", "") for bando in bandi_compatibili]
        lista_bandi_testo = "\n".join(titoli_bandi)

        prompt = (
            f"Di seguito trovi l’analisi completa dell’azienda e l’elenco dei bandi compatibili trovati:\n\n"
            f"📊 ANALISI AZIENDALE:\n{analisi_gpt}\n\n"
            f"📂 BANDI COMPATIBILI:\n{lista_bandi_testo}\n\n"
            f"Analizza il tutto e fornisci da 1 a 10 soluzioni strategiche e concrete per migliorare l’impresa, sia dal punto di vista economico-finanziario sia in termini di efficienza. Evita premesse inutili."
        )

        risposta = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=MAX_CARATTERI,
            temperature=0.6,
            system="Sei un CFO esperto in analisi aziendale, merito creditizio e strategia. Ricevi output GPT e lista bandi, poi suggerisci fino a 10 azioni concrete per migliorare l’azienda.",
            messages=[{"role": "user", "content": prompt}]
        )

        risposta_finale = risposta.content[0].text[:MAX_CARATTERI]

        # Tracciamento salvataggio
        with open("output_claude.txt", "w") as file:
            file.write(risposta_finale)

        print("🟢 Relazione Claude generata correttamente.")
        return risposta_finale

    except Exception as e:
        print("🔴 Errore durante la generazione della relazione con Claude:", e)
        return "Errore durante la generazione della relazione con Claude"
