def genera_relazione_con_claude(analisi_gpt: str, caratteristiche: dict, bandi: list) -> str:
    try:
        logging.info("🤖 Claude sta confrontando l'analisi GPT con i bandi disponibili...")

        caratteristiche_text = f"""
L'azienda presenta le seguenti caratteristiche ufficiali:
- Regione: {caratteristiche.get("regione", "N/D")}
- Provincia: {caratteristiche.get("provincia", "N/D")}
- Codice ATECO: {caratteristiche.get("codice_ateco", "N/D")}
- Forma giuridica: {caratteristiche.get("forma_giuridica", "N/D")}
- Amministratore: {caratteristiche.get("amministratore", "N/D")}
- Denominazione: {caratteristiche.get("denominazione", "N/D")}
"""

        prompt = caratteristiche_text + f"""

📊 Analisi economico-finanziaria dell'impresa (GPT):

{analisi_gpt}

📋 I bandi compatibili trovati sono:

{formatta_bandi(bandi)}

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
