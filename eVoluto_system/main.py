from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from pathlib import Path
from estrazione_pdf import estrai_testo_da_pdf
from gpt_module import analisi_tecnica_gpt

app = FastAPI()

OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

@app.post("/analizza-pdf/")
async def analizza_pdf(file: UploadFile = File(...)):
    try:
        pdf_path = OUTPUT_DIR / file.filename
        with open(pdf_path, "wb") as f:
            content = await file.read()
            f.write(content)

        testo = estrai_testo_da_pdf(pdf_path)
        if not testo:
            return JSONResponse(status_code=400, content={"message": "Nessun testo estratto dal PDF."})

        # Esegui l'analisi
        visura = estrai_visura(testo)
        preventivi = estrai_preventivi(testo)
        piano_ammortamento = estrai_piano_ammortamento(testo)
        analisi_result = analisi_tecnica_gpt(testo, visura, preventivi, piano_ammortamento)

        return JSONResponse(status_code=200, content={"message": "Analisi completata", "data": analisi_result})

    except Exception as e:
        return JSONResponse(status_code=500, content={"message": f"Errore: {str(e)}"})

@app.get("/")
def read_root():
    return {"message": "Servizio attivo. Invia un file PDF per l'analisi."}

# Placeholder
def estrai_visura(testo): return "Visura simulata"
def estrai_preventivi(testo): return "Preventivi simulati"
def estrai_piano_ammortamento(testo): return "Piano simulato"
