from fastapi import FastAPI
from fastapi.responses import JSONResponse
import os
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

        # Esegui l'analisi GPT con parametri opzionali
        visura = estrai_visura(testo) if testo else None  # Optional
        preventivi = estrai_preventivi(testo) if testo else None  # Optional
        piano_ammortamento = estrai_piano_ammortamento(testo) if testo else None  # Optional

        # Chiamata alla funzione analisi_gpt con i parametri opzionali
        analisi_result = analisi_tecnica_gpt(testo, visura=visura, preventivi=preventivi, piano_ammortamento=piano_ammortamento)

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

# Funzione per estrarre la visura dal testo del PDF (opzionale)
def estrai_visura(testo: str):
    # Logica per estrarre la visura dal testo
    # Restituisce un dato simulato per visura come esempio
    visura = "Visura estratta dal documento"
    return visura

# Funzione per estrarre i preventivi dal testo del PDF (opzionale)
def estrai_preventivi(testo: str):
    # Logica per estrarre i preventivi dal testo
    # Restituisce un dato simulato per preventivi come esempio
    preventivi = "Preventivi associati trovati nel documento"
    return preventivi

# Funzione per estrarre il piano di ammortamento dal testo del PDF (opzionale)
def estrai_piano_ammortamento(testo: str):
    # Logica per estrarre il piano di ammortamento dal testo
    # Restituisce un dato simulato per piano_ammortamento come esempio
    piano_ammortamento = "Piano di ammortamento trovato nel documento"
    return piano_ammortamento
