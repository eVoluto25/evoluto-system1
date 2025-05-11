from typing import Optional
from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import JSONResponse
from pathlib import Path

app = FastAPI()
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

@app.post("/analizza-pdf/")
async def analizza_pdf(
    name: Optional[str] = Form(None, alias="name-2"),
    phone: Optional[str] = Form(None, alias="phone-1"),
    email: Optional[str] = Form(None, alias="email-1"),
    file: Optional[UploadFile] = Form(None, alias="upload-1")
):
    try:
        file_info = None
        if file:
            file_path = OUTPUT_DIR / file.filename
            with open(file_path, "wb") as f:
                f.write(await file.read())
            file_info = file.filename

        return JSONResponse(status_code=200, content={
            "message": "Dati ricevuti.",
            "nome": name,
            "telefono": phone,
            "email": email,
            "file_salvato": file_info
        })
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/")
def read_root():
    return {"message": "Servizio attivo. Invia un file PDF per l'analisi."}
