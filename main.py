from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import JSONResponse
from pathlib import Path
from datetime import datetime
import os

from pipeline import elabora_pipeline  # ⬅️ nome funzione corretto

app = FastAPI()

@app.post("/analizza-pdf")
async def analizza_pdf(
    name: str = Form(..., alias="name-2"),
    phone: str = Form(..., alias="phone-1"),
    email: str = Form(..., alias="email-1"),
    upload: UploadFile = Form(..., alias="upload-1")
):
    try:
        # Crea cartella output/ se non esiste
        output_dir = Path("output")
        output_dir.mkdir(parents=True, exist_ok=True)

        # Salva il file come documento.pdf (fisso)
        upload_path = output_dir / "documento.pdf"
        with open(upload_path, "wb") as f:
            f.write(await upload.read())

        # Avvia l’elaborazione coerente
        elabora_pipeline(nome_azienda=name)  # ⬅️ variabile standard

        return JSONResponse(content={
            "status": "ok",
            "message": "Dati ricevuti, analisi in corso"
        })

    except Exception as e:
        return JSONResponse(status_code=500, content={
            "status": "error",
            "message": str(e)
        })
