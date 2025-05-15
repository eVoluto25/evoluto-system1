import logging
import sys
from fastapi import FastAPI, UploadFile, Form, File
from fastapi.responses import JSONResponse
import uvicorn
from pipeline import esegui_pipeline

logging.basicConfig(level=logging.INFO)
app = FastAPI()

@app.get("/")
def home():
    return {"message": "Server attivo. eVoluto System live."}


@app.post("/analizza-pdf")
async def analizza_pdf(upload_1: UploadFile = File(...), email_1: str = Form(...)):
    file = upload_1
    email = email_1  # riassegno per compatibilità
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

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=10000)
