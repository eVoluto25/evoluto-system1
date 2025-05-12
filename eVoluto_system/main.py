from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import JSONResponse
from pathlib import Path
import os
from datetime import datetime, timedelta

from pipeline import esegui_analisi_completa
from bandi_tracker.download_bandi import download_bandi  # ✅ Corretto qui

# 🔧 Configurazione FastAPI
app = FastAPI()

# 📁 Directory di output per i file ricevuti
OUTPUT_DIR = Path("estratti_pdf")
OUTPUT_DIR.mkdir(exist_ok=True)

# ✅ Endpoint principale per il form
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

        # 🧠 Avvia l’analisi completa
        risultato = esegui_analisi_completa(file_path, nome_azienda=name)

        return JSONResponse(status_code=200, content={
            "message": "Analisi completata con successo.",
            "azienda": name,
            "file": file.filename
        })

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


# ✅ Endpoint opzionale per aggiornare i bandi
@app.get("/aggiorna-bandi/")
def aggiorna_bandi():
    try:
        download_bandi()
        return JSONResponse(status_code=200, content={
            "message": "Download bandi eseguito correttamente.",
            "timestamp": str(datetime.now())
        })
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
