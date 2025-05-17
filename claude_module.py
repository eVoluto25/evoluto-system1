import logging
import os
import anthropic
from bandi_utils import aggiorna_bandi
from storage_handler import upload_html_to_supabase

anthropic.api_key = os.getenv("ANTHROPIC_API_KEY")

def genera_relazione_con_claude(analisi_gpt: str, caratteristiche_azienda: dict, bandi: list) -> str:
    try:
        logging.info("🤖 Claude sta confrontando l'analisi GPT con i bandi disponibili...")

        caratteristiche_text = f"""
L'azienda presenta le seguenti caratteristiche ufficiali:
- Regione: {caratteristiche_azienda.get("regione", "N/D")}
- Provincia: {caratteristiche_azienda.get("provincia", "N/D")}
- Codice ATECO: {caratteristiche_azienda.get("codice_ateco", "N/D")}
- Forma giuridica: {caratteristiche_azienda.get("forma_giuridica", "N/D")}
- Amministratore: {caratteristiche_azienda.get("amministratore", "N/D")}
- Denominazione: {caratteristiche_azienda.get("denominazione", "N/D")}
"""

        prompt = caratteristiche_text + f"""

📊 Analisi economico-finanziaria dell'impresa (GPT):

{analisi_gpt}

📋 I bandi compatibili trovati sono:

{aggiorna_bandi(bandi)}

🧠 Elabora una relazione sintetica che identifichi:
1. I bandi più coerenti con la situazione economica dell’azienda
2. Perché sono rilevanti
3. Quali benefici potrebbe ottenere
4. Se l’azienda ha le caratteristiche per sostenerli economicamente (es. DSCR, rating, co-finanziamento, struttura costi/ricavi)
5. Se ci sono rischi da considerare o alternative disponibili
6. Se l’azienda può usare il bando anche per coprire debiti o rientri bancari
7. Se può ottenere un anticipo su affidamento

🔍 Dai un voto alla compatibilità (alta, media, bassa) e alla probabilità di successo (alta, media, bassa).

📌 Ordina per priorità i primi 5 bandi, poi elenca gli altri come "altri bandi compatibili".

💬 Usa uno stile professionale, sintetico e numerato.

📄 Restituisci il testo in HTML ordinato, usando <h2> per i titoli e <p> per i paragrafi.
"""

        return prompt

    except Exception as e:
        logging.error(f"❌ Errore Claude → {e}")
        return "Errore durante il confronto con i bandi."
