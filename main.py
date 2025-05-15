import logging
import os
from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import JSONResponse
from extractor import estrai_dati_da_pdf
from gpt_module import analizza_completo_con_gpt
from claude_module import genera_relazione_con_claude
from pipeline import aggiorna_bandi, esegui_analisi_completa
from moduli.make_webhook import invia_a_make

app = FastAPI()
@app.api_route("/", methods=["GET", "HEAD"])
def root_head():
    return {"status": "✅ eVoluto backend attivo", "version": "1.0"}

@app.post("/analizza-pdf")
async def analizza_pdf(
    upload_1: UploadFile = Form(...),   # questo riceve il PDF
    email_1: str = Form(...)            # questo riceve l'email
):
    logging.info("✅ Ricevuto upload_1: %s, email_1: %s", upload_1.filename, email_1)
    
    # Salvataggio file temporaneo
    temp_file_path = "temp_file.pdf"
    with open(temp_file_path, "wb") as f:
        f.write(await upload_1.read())

    try:
        logging.info("🚀 Inizio pipeline completa")

        # Estrazione dati da visura PDF
        caratteristiche_azienda, bilancio = estrai_dati_da_pdf(temp_file_path)
        logging.info("📄 Estrazione dati completata")

        # Validazione base
        if not caratteristiche_azienda or not bilancio:
            logging.error("❌ Dati aziendali o bilancio mancanti o vuoti")
            return JSONResponse(status_code=422, content={"errore": "Dati insufficienti"})

        # Analisi GPT
        logging.info("🤖 Chiamata a GPT in corso...")
        analisi_finanziaria = analizza_completo_con_gpt(bilancio)

        if not analisi_finanziaria or analisi_finanziaria.strip() == "":
            logging.error("❌ GPT ha restituito una risposta vuota o nulla.")
            return JSONResponse(status_code=422, content={"errore": "Analisi GPT non riuscita"})

        # Aggiornamento bandi pubblici
        try:
            logging.info("🛰 Aggiornamento bandi pubblici in corso")
            aggiorna_bandi()
        except Exception as e:
            logging.warning(f"⚠ Impossibile aggiornare bandi: {e}")

        # Matching con bandi disponibili
        logging.info("📊 Avvio matching con i bandi disponibili")
        bandi_compatibili = esegui_analisi_completa(caratteristiche_azienda, bilancio)

        # Analisi Claude (relazione)
        logging.info("📎 Generazione relazione finale tramite Claude")
        relazione_finale = genera_relazione_con_claude(analisi_finanziaria, bandi_compatibili)

        # Pulizia file temporaneo
        os.remove(temp_file_path)

        # Pulizia file temporaneo
os.remove(temp_file_path)

# Costruzione payload da inviare a Make
payload = {
    "denominazione": caratteristiche_azienda.get("denominazione", "N/D"),
    "amministratore": caratteristiche_azienda.get("amministratore", "N/D"),
    "outputGpt": link_gpt,
    "outputClaude": link_claude
}

# Invio al webhook Make
try:
    response = requests.post("https://hook.eu2.make.com/tuo_webhook", json=payload)
    response.raise_for_status()
    print("✅ Dati inviati correttamente a Make.")
except requests.exceptions.RequestException as e:
    print(f"❌ Errore invio Make: {e}")

# Restituzione risposta finale

        return {
            "analisi": analisi_finanziaria,
            "bandi": bandi_compatibili,
            "relazione": relazione_finale
        try:
            # Pulizia file temporaneo
            os.remove(temp_file_path)
        except Exception as e:
           logging.warning(f"⚠️ Impossibile rimuovere il file temporaneo: {e}")

        # Restituzione risposta finale
        return {
            "analisi": analisi_finanziaria,
            "bandi": bandi_compatibili,
            "relazione": relazione_finale
        }
