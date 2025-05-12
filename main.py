import logging
logging.basicConfig(level=logging.INFO)
from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import JSONResponse
from pathlib import Path
from datetime import datetime
import os

from pipeline import esegui_analisi_completa  # Usa il nome reale presente nel tuo sistema

app = FastAPI()

@app.post("/analizza-pdf")
async def analizza_pdf(
    name: str = Form(..., alias="name_2"),
    phone: str = Form(..., alias="phone_1"),
    email: str = Form(..., alias="email_1"),
    upload: UploadFile = Form(..., alias="upload_1")
):
    try:
        logging.info(f"➡️ Richiesta ricevuta: name={name}, phone={phone}, email={email}, file={upload.filename}")
        # Cartella di salvataggio coerente con il sistema
        output_dir = Path("output")
        output_dir.mkdir(parents=True, exist_ok=True)

        # Salva file sempre come documento.pdf
        upload_path = output_dir / "documento.pdf"
        with open(upload_path, "wb") as f:
            f.write(await upload.read())

        # Lancia la pipeline con i nomi giusti
        esegui_analisi_completa(upload_path, name)

        return JSONResponse(content={
            "status": "ok",
            "message": "Dati ricevuti, analisi avviata"
        })

    except Exception as e:
        logging.error("❌ Errore interno nel backend")
        logging.exception(e)
        return JSONResponse(status_code=500, content={
            "status": "error",
            "message": str(e)
        })
