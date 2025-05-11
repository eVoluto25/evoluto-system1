from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import JSONResponse
from pathlib import Path

app = FastAPI()

OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

@app.post("/analizza-pdf/")
async def analizza_pdf(
    name: str = Form(..., alias="name-2"),
    phone: str = Form(..., alias="phone-1"),
    email: str = Form(..., alias="email-1"),
    file: UploadFile = Form(..., alias="upload-1")
):
    try:
        file_path = OUTPUT_DIR / file.filename
        with open(file_path, "wb") as f:
            f.write(await file.read())

        return JSONResponse(status_code=200, content={
            "message": "File ricevuto con successo.",
            "nome": name,
            "telefono": phone,
            "email": email,
            "file_salvato": file.filename
        })
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/")
def read_root():
    return {"message": "Servizio attivo. Invia un file PDF per l'analisi."}
