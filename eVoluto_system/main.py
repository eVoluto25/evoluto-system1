from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from pathlib import Path
import shutil

from estrazione_pdf import estrai_testo_da_pdf
from gpt_module import analisi_tecnica_gpt

app = FastAPI()

OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

@app.post("/upload/")
async def upload_pdf(
    nome: str = Form(...),
    cognome: str = Form(...),
    telefono: str = Form(...),
    email: str = Form(...),
    file: UploadFile = File(...)
):
    try:
        pdf_path = OUTPUT_DIR / f"{nome}_{cognome}.pdf"
        with open(pdf_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        testo = estrai_testo_da_pdf(pdf_path)
        if not testo:
            return JSONResponse(status_code=400, content={"message": "Nessun testo estratto dal PDF."})

        visura = estrai_visura(testo)
        preventivi = estrai_preventivi(testo)
        piano_ammortamento = estrai_piano_ammortamento(testo)

        analisi_result = analisi_tecnica_gpt(testo, visura=visura, preventivi=preventivi, piano_ammortamento=piano_ammortamento)

        output_gpt_path = OUTPUT_DIR / f"analisi_{nome}_{cognome}.txt"
        with open(output_gpt_path, "w") as f:
            f.write(analisi_result)

        return {"message": "Analisi completata con successo", "analisi": analisi_result}

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/")
def read_root():
    return {"message": "Servizio attivo. Invia un file PDF per l'analisi."}

def estrai_visura(testo: str):
    return "Visura simulata estratta dal testo"

def estrai_preventivi(testo: str):
    return "Preventivi simulati trovati nel testo"

def estrai_piano_ammortamento(testo: str):
    return "Piano di ammortamento simulato trovato nel testo"
