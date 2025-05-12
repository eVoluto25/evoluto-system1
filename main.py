from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import JSONResponse
from pathlib import Path
import os

from pipeline import esegui_analisi_completa
from datetime import datetime

app = FastAPI()

@app.post("/")
async def analizza_pdf(
    file: UploadFile = Form(..., alias="upload-1"),
    nome: str = Form(..., alias="name-2"),
    email: str = Form(..., alias="email-1"),
    telefono: str = Form(..., alias="phone-1")
):
    # Percorso output temporaneo
    OUTPUT_DIR = Path("estratti_pdf")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    percorso_pdf = OUTPUT_DIR / f"{datetime.utcnow().timestamp()}_{file.filename}"

    # Salva il PDF temporaneamente
    with open(percorso_pdf, "wb") as f:
        f.write(await file.read())

    # Esegue l’analisi completa
    try:
        risultato = esegui_analisi_completa(percorso_pdf, nome_azienda=nome)
        return JSONResponse(content={
            "successo": True,
            "messaggio": "Analisi completata con successo.",
            "output": risultato
        })
    except Exception as e:
        return JSONResponse(content={
            "successo": False,
            "errore": str(e)
        }, status_code=500)
