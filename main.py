from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import JSONResponse
from pathlib import Path
import os

from pipeline import esegui_analisi_completa
from datetime import datetime

app = FastAPI()

@app.post("/analizza-pdf/")
async def analizza_pdf_endpoint(file: UploadFile, nome_azienda: str = Form(...)):
    """
    Endpoint riceve PDF da Forminator e avvia l'analisi completa.
    """
    try:
        # Salva il file PDF nella directory degli estratti
        input_path = Path("estratti_pdf") / f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{file.filename}"
        input_path.parent.mkdir(parents=True, exist_ok=True)

        with open(input_path, "wb") as f:
            content = await file.read()
            f.write(content)

        # Avvia l'analisi
        output = esegui_analisi_completa(file_path=input_path, nome_azienda=nome_azienda)

        return JSONResponse(content={"status": "ok", "output": output})

    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "detail": str(e)})
