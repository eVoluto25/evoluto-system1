import os
import logging
import openai  # minuscolo, corretto

def genera_relazione_con_claude(analisi_gpt: str, caratteristiche: dict, bandi: list) -> str:
    try:
        logging.info("🤖 Claude sta confrontando l'analisi GPT con i bandi disponibili...")

        prompt = (
            f"Hai ricevuto un'analisi finanziaria dell'azienda basata sul suo bilancio:\n\n"
            f"📊 Analisi GPT:\n{analisi_gpt}\n\n"
            f"L'azienda ha queste caratteristiche:\n"
            f"- Forma giuridica: {caratteristiche.get('forma_giuridica')}\n"
            f"- Codice ATECO: {caratteristiche.get('codice_ateco')}\n"
            f"- Attività prevalente: {caratteristiche.get('attivita_prevalente')}\n\n"
            f"I bandi compatibili trovati sono:\n"
            f"{formatta_bandi(bandi)}\n\n"
            f"🎯 Elabora una relazione sintetica che identifichi:\n"
            f"1. I bandi più coerenti con la situazione economica dell’azienda\n"
            f"2. Perché sono rilevanti\n"
            f"3. Quali benefici potrebbe ottenere\n"
            f"Usa uno stile chiaro, professionale e numerato."
        )

        openai.api_key = os.getenv("OPENAI_API_KEY")
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4
        )

        return response.choices[0].message["content"]

    except Exception as e:
        logging.error(f"❌ Errore Claude → {e}")
        return "Errore durante il confronto con i bandi."

def formatta_bandi(bandi: list) -> str:
    if not bandi:
        return "❌ Nessun bando disponibile per l’azienda."

    righe = []
    for bando in bandi:
        righe.append(
            f"🔹 {bando.get('titolo', 'Titolo non disponibile')} — "
            f"Contributo: {bando.get('contributo', 'N/D')} — "
            f"Scadenza: {bando.get('scadenza', 'N/D')}"
        )
    return "\n".join(righe)
