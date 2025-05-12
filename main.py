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
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"{timestamp}_{upload.filename}"
        filepath = Path(f"/tmp/{filename}")

        with open(filepath, "wb") as f:
            f.write(await upload.read())

        logging.info(f"🟢 RICEVUTA: {name}, {phone}, {email}, file={filename}")

        # Esegui analisi (opzionale)
        esegui_analisi_completa(filepath)

        return JSONResponse(content={"esito": "ok"})
    except Exception as e:
        logging.error(f"Errore: {e}")
        return JSONResponse(content={"esito": "errore", "messaggio": str(e)}, status_code=500)
