from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from pathlib import Path
from estrazione_pdf import estrai_testo_da_pdf
from gpt_module import analisi_tecnica_gpt

app = FastAPI()

OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

@app.post("/upload/")
async def ricevi_dal_form(
    nome: str = Form(...),
    cognome: str = Form(...),
    telefono: str = Form(...),
    email: str = Form(...),
    file: UploadFile = File(...)
):
    try:
        # Salva PDF su disco
        pdf_path = OUTPUT_DIR / file.filename
        content = await file.read()
        with open(pdf_path, "wb") as f:
            f.write(content)

        # Estrazione testo
        testo = estrai_testo_da_pdf(pdf_path)
        if not testo:
            return JSONResponse(status_code=400, content={"message": "PDF vuoto o non leggibile"})

        # Estrazione opzionale
        visura = estrai_visura(testo)
        preventivi = estrai_preventivi(testo)
        piano_ammortamento = estrai_piano_ammortamento(testo)

        # Analisi GPT
        analisi = analisi_tecnica_gpt(testo, visura=visura, preventivi=preventivi, piano_ammortamento=piano_ammortamento)

        # Salva risultato
        output_path = OUTPUT_DIR / f"{file.filename}_output.txt"
        with open(output_path, "w") as f:
            f.write(analisi)

        return JSONResponse(content={
            "message": "Analisi completata",
            "cliente": f"{nome} {cognome}",
            "telefono": telefono,
            "email": email,
            "file": file.filename
        })

    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})

@app.get("/")
def home():
    return {"message": "Servizio attivo. Invia un file PDF per l'analisi."}

def estrai_visura(testo: str):
    return "Visura estratta dal documento"

def estrai_preventivi(testo: str):
    return "Preventivi trovati nel documento"

def estrai_piano_ammortamento(testo: str):
    return "Piano di ammortamento rilevato"
