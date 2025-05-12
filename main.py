from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import JSONResponse
from pathlib import Path
import os
from pipeline import esegui_analisi_completa

app = FastAPI()

@app.post("/analizza-pdf")
async def analizza_pdf(
    name: str = Form(..., alias="name-2"),
    phone: str = Form(..., alias="phone-1"),
    email: str = Form(..., alias="email-1"),
    upload: UploadFile = Form(..., alias="upload-1")
):
    # Salva il file
    upload_path = Path("estratti_pdf") / upload.filename
    with open(upload_path, "wb") as f:
        f.write(await upload.read())

    # Avvia l’analisi completa
    output = esegui_analisi_completa(upload_path, name)

    return JSONResponse(content={"status": "ok", "message": "Analisi ricevuta", "output": output})


        # Logica temporanea per confermare ricezione
        print("Ricevuto:", nome, email)

        return {"status": "success", "message": "Dati ricevuti correttamente"}

    except Exception as e:
        return {"status": "error", "message": str(e)}
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

        @app.post("/")
async def ricevi_dal_form_root(file: UploadFile = File(...), nome_azienda: str = Form(...)):
    # fallback per i form che inviano su dominio root
    print("Ricevuto file dal form root")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    percorso_file = OUTPUT_DIR / file.filename
    with open(percorso_file, "wb") as f:
        f.write(await file.read())

    print(f"File salvato in: {percorso_file}")

    risultato = esegui_analisi_completa(percorso_file, nome_azienda)
    print(f"Risultato analisi: {risultato}")

    return JSONResponse(content={"esito": "ricevuto", "analisi": risultato})
