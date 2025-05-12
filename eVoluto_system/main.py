from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import JSONResponse
from pathlib import Path
import os
from pipeline import esegui_analisi_completa
from bandi_tracker.download_bandi import download_bandi
from datetime import datetime, timedelta

app = FastAPI()

OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 🔁 Controllo aggiornamento bandi
def check_aggiornamento_bandi():
    percorso_file = Path("bandi_tracker/dataset_bandi.csv")
    giorni_limite = 15

    if not percorso_file.exists():
        print("🟡 File bandi non trovato. Avvio download...")
        download_bandi()
        return

    ultima_modifica = datetime.fromtimestamp(os.path.getmtime(percorso_file))
    giorni_passati = (datetime.now() - ultima_modifica).days

    if giorni_passati >= giorni_limite:
        print(f"🔁 Sono passati {giorni_passati} giorni. Avvio aggiornamento bandi.")
        download_bandi()
    else:
        print(f"✅ File bandi aggiornato {giorni_passati} giorni fa. Nessun aggiornamento necessario.")

# ✅ Endpoint principale: trigger + verifica bandi
@app.get("/")
def read_root():
    check_aggiornamento_bandi()
    return {"message": "Servizio attivo. Verifica bandi completata."}

# ✅ Endpoint ricezione file e dati via form
@app.post("/analizza-pdf/")
async def analizza_pdf(
    name: str = Form(..., alias="name-2"),
    phone: str = Form(..., alias="phone-1"),
    email: str = Form(..., alias="email-1"),
    file: UploadFile = Form(..., alias="upload-1")
):
    try:
        file_path = OUTPUT_DIR / file.filename
        with open(file_path, "wb") as f:
            f.write(await file.read())

        # Esegue l’analisi + invio email a info@capitaleaziendale.it
        risultato = esegui_analisi_completa(file_path, nome_azienda=name)

        return JSONResponse(status_code=200, content={
            "message": "Analisi completata con successo.",
            "azienda": name,
            "file": file.filename
        })

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
