
import logging
logging.basicConfig(level=logging.INFO)

from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import JSONResponse
from pathlib import Path
from datetime import datetime
import os

from pipeline import esegui_analisi_completa  # Non viene richiamata per ora

app = FastAPI()

@app.get("/")
def test():
    return {"status": "API online"}

@app.post("/analizza-pdf")
async def analizza_pdf(
    name: str = Form(..., alias="name_2"),
    phone: str = Form(..., alias="phone_1"),
    email: str = Form(..., alias="email_1"),
    upload: UploadFile = Form(..., alias="upload_1")
):
    logging.info(f"🟢 RICEVUTA: {name}, {phone}, {email}, file={upload.filename}")
    return {"status": "ricevuto"}
