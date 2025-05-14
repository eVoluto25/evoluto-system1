import logging
import sys
from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import JSONResponse
import uvicorn
from pipeline import esegui_pipeline
import os

logging.basicConfig(level=logging.INFO)
app = FastAPI()

# CLI fallback
def avvia_analisi_da_terminale():
    if len(sys.argv) != 3:
        print("Uso: python main.py <percorso_pdf> <email_destinatario>")
        return
    percorso = sys.argv[1]
    email = sys.argv[2]
    logging.info(f"▶️ Avvio pipeline da terminale con: {percorso}, {email}")
    esegui_pipeline(percorso, email)

# API endpoint
@app.post("/analizza-pdf")
async def analizza_pdf(file: UploadFile, email: str = Form(...)):
    try:
        nome_file = f"temp_{file.filename}"
        with open(nome_file, "wb") as f:
            f.write(await file.read())
        logging.info(f"📥 File ricevuto via API: {nome_file}, email: {email}")
        esegui_pipeline(nome_file, email)
        return JSONResponse(content={"status": "ok", "file": nome_file})
    except Exception as e:
        logging.error(f"❌ Errore endpoint /analizza-pdf: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})

# Auto-avvio da CLI se eseguito direttamente
if __name__ == "__main__":
    if len(sys.argv) > 1:
        avvia_analisi_da_terminale()
    else:
        uvicorn.run("main:app", host="0.0.0.0", port=10000)
