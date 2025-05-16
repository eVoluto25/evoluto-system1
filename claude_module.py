import os
import logging
import openai  # minuscolo, corretto
from storage_handler import upload_html_to_supabase
from datetime import datetime

def genera_relazione_con_claude(analisi_gpt: str, caratteristiche: dict, bandi: list) -> str:
    try:
        logging.info("🤖 Claude sta confrontando l'analisi GPT con i bandi disponibili...")
      
    f"L'azienda presenta le seguenti caratteristiche ufficiali:"
    - Regione: {caratteristiche.get("regione", "N/D")}
    - Provincia: {caratteristiche.get("provincia", "N/D")}
    - Codice ATECO: {caratteristiche.get("codice_ateco", "N/D")}
    - Forma giuridica: {caratteristiche.get("forma_giuridica", "N/D")}
    - Amministratore: {caratteristiche.get("amministratore", "N/D")}
    - Denominazione: {caratteristiche.get("denominazione", "N/D")}
"""

    f"📊 Analisi economico-finanziaria dell'impresa (GPT):
{analisi_gpt}

"
    f"📁 Elenco bandi compatibili individuati:
{formatta_bandi(bandi)}

"

    f"🎯 Il tuo compito è redigere una relazione tecnico-strategica per identificare le migliori opportunità pubbliche per questa azienda, valutando i bandi trovati.

"

    f"Per ciascun bando, esegui questa valutazione in 5 punti:
"
    f"1. Verifica l'ammissibilità formale dell'impresa (forma giuridica, territorio, settore, codice ATECO)
"
    f"2. Valuta la coerenza tra finalità del bando e l’analisi economico-finanziaria dell’impresa (es. ROI, DSCR, EBITDA, indebitamento, flusso di cassa, sostenibilità debito)
"
    f"3. Se disponibile, usa il giudizio ESG espresso da GPT per consigliare bandi green/sostenibili
"
    f"4. Assegna un punteggio alla probabilità di successo nel vincere il bando, da ⭐ a ⭐⭐⭐⭐⭐ (basato su coerenza economica, tecnica, rating e livello di concorrenza previsto)
"
    f"5. Se ci sono più di 5 bandi, seleziona e classifica i 5 più vantaggiosi, indicando: 1° più rilevante, fino al 5° (per impatto economico e facilità di attivazione)

"

    f"📝 Riporta il tutto in formato HTML ordinato:
"
    f"- Usa <h2> per i titoli delle sezioni
"
    f"- Usa <h3> per ogni bando analizzato
"
    f"- Usa <p> e <ul><li> per descrivere punti e analisi
"
    f"- Evidenzia <strong> i dati principali e le raccomandazioni finali
"
    f"💡 Dopo aver analizzato i primi 5 bandi più coerenti, elenca in fondo alla relazione anche tutti gli altri bandi compatibili rimasti (senza commento), come riepilogo. Indica per ciascuno solo titolo.\n"
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
