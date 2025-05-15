import os
import logging
import openai  # minuscolo, corretto
from moduli.storage_supabase import upload_claude_to_supabase
from datetime import datetime

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
            f"Restituisci tutto in formato HTML ordinato, usando <h2> per i titoli di sezione e <p> per i paragrafi."
        )

        openai.api_key = os.getenv("OPENAI_API_KEY")
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4
        )

def upload_claude_to_supabase(contenuto_html: str, nome_file: str) -> str:
    import os
    import requests

    supabase_url = os.getenv("SUPABASE_URL")
    supabase_bucket = os.getenv("SUPABASE_BUCKET")
    supabase_api_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

    if not all([supabase_url, supabase_bucket, supabase_api_key]):
        raise EnvironmentError("Variabili d'ambiente Supabase mancanti")

    headers = {
        "Authorization": f"Bearer {supabase_api_key}",
        "Content-Type": "text/html"
    }

    path_remoto = f"output_claude/{nome_file}.html"
    url_upload = f"{supabase_url}/storage/v1/object/{supabase_bucket}/{path_remoto}"

    response = requests.put(url_upload, headers=headers, data=contenuto_html.encode("utf-8"))
    if response.status_code not in [200, 201]:
        raise RuntimeError(f"Errore upload Claude: {response.status_code} - {response.text}")

    url_pubblico = f"{supabase_url}/storage/v1/object/public/{supabase_bucket}/{path_remoto}"
      
       contenuto_html = response.choices[0].message["content"]
       nome_file = f"output_claude_{datetime.now().strftime('%Y%m%d%H%M%S')}.html"
       return upload_claude_to_supabase(contenuto_html, nome_file)

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
