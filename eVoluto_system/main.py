from fastapi import FastAPI
from fastapi.responses import JSONResponse
import os
import shutil
from estrazione_pdf import estrai_testo_da_pdf  # Assicurati che questa funzione esista e sia corretta
from gpt_module import analisi_tecnica_gpt  # Importa la tua funzione GPT
from pathlib import Path

app = FastAPI()

# Definiamo il percorso della cartella output
OUTPUT_DIR = Path("output")
if not OUTPUT_DIR.exists():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

@app.post("/analizza-pdf/")
async def analizza_pdf(file: bytes):
    try:
        # Salva il file ricevuto
        pdf_path = OUTPUT_DIR / "documento.pdf"
        with open(pdf_path, "wb") as f:
            f.write(file)
        
        # Estrazione testo dal PDF
        testo = estrai_testo_da_pdf(pdf_path)
        if not testo:
            return JSONResponse(status_code=400, content={"message": "Nessun testo estratto dal PDF."})

        # Esegui l'analisi GPT
        visura = "Dati visura estratti"  # Sostituisci con i dati reali estratti dal PDF o altre fonti
        preventivi = "Preventivi associati"  # Sostituisci con i dati reali
        analisi_result = analisi_tecnica_gpt(testo, visura, preventivi)

        # Salvataggio dell'output GPT in un file di testo
        output_gpt_path = OUTPUT_DIR / "output_gpt.txt"
        with open(output_gpt_path, "w") as f:
            f.write(analisi_result)

        return JSONResponse(status_code=200, content={"message": "Analisi completata con successo.", "data": analisi_result})

    except Exception as e:
        return JSONResponse(status_code=500, content={"message": f"Errore durante l'elaborazione: {str(e)}"})

@app.get("/")
def read_root():
    return {"message": "Servizio attivo. Invia un file PDF per l'analisi."}
