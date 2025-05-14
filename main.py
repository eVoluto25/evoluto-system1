import logging
logging.basicConfig(level=logging.INFO)
from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import JSONResponse
from pathlib import Path
from datetime import datetime
import os

from pipeline import esegui_analisi_completa

app = FastAPI()

@app.api_route("/", methods=["GET", "HEAD"])
async def root():
    return {"status": "ok"}
    
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
        upload_folder = Path("uploads")
        upload_folder.mkdir(exist_ok=True)
        Path("uploads").mkdir(parents=True, exist_ok=True)
        path = Path("uploads") / filename
        with open(path, "wb") as f:
            f.write(await upload.read())
        logging.info(f"🟢 RICEVUTA: {name}, {phone}, {email}, file={upload.filename}")
        logging.info("🧠 Avvio esecuzione completa: GPT + Claude")
        esegui_analisi_completa(path, {"nome": name, "email": email, "telefono": phone}, "dataset_bandi.csv")
        logging.info("✅ Esecuzione completa terminata.")
        return JSONResponse(content={"esito": "ok"})
    except Exception as e:
        logging.error(f"Errore durante l'elaborazione: {e}")
        return JSONResponse(content={"esito": "errore", "dettaglio": str(e)}, status_code=500)
