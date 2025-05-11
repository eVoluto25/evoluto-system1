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
        # Salva il file PDF
        pdf_path = OUTPUT_DIR / file.filename
        with open(pdf_path, "wb") as f:
            content = await file.read()
            f.write(content)

        # Estrai testo dal PDF
        testo = estrai_testo_da_pdf(pdf_path)
        if not testo:
            return JSONResponse(status_code=400, content={"message": "Nessun testo estratto dal PDF."})

        # Analisi con GPT
        analisi_result = analisi_tecnica_gpt(testo)

        # Salva output
        output_path = OUTPUT_DIR / "output_gpt.txt"
        with open(output_path, "w") as f:
            f.write(analisi_result)

        return JSONResponse(status_code=200, content={"message": "Analisi completata.", "risultato": analisi_result})

    except Exception as e:
        return JSONResponse(status_code=500, content={"message": f"Errore interno: {str(e)}"})

@app.get("/")
def read_root():
    return {"message": "Servizio attivo. Invia un file PDF per l'analisi via POST."}
