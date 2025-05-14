from fastapi import FastAPI, Form, UploadFile
from fastapi.responses import JSONResponse
import logging
import os
from datetime import datetime
from pathlib import Path
from pipeline import esegui_analisi_completa
from claude_module import genera_relazione_con_claude

app = FastAPI()

# ✅ Health check semplice
@app.api_route("/", methods=["GET", "HEAD"])
def root():
    return {"status": "ok"}

# ✅ Endpoint principale di analisi
@app.post("/analizza-pdf")
async def analizza_pdf(
    name: str = Form(..., alias="name_2"),
    phone: str = Form(..., alias="phone_1"),
    email: str = Form(..., alias="email_1"),
    upload: UploadFile = Form(..., alias="upload_1")
):
    try:
        # Salvataggio file
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"{timestamp}_{upload.filename}"
        upload_folder = Path("uploads")
        upload_folder.mkdir(parents=True, exist_ok=True)
        path = upload_folder / filename

        with open(path, "wb") as f:
            f.write(await upload.read())

        logging.info(f"🟢 RICEVUTA: {name}, {phone}, {email}, file={upload.filename}")

        # Verifica se esiste già la relazione Claude
        if os.path.exists("relazione_finale.txt"):
            logging.info("📄 Relazione Claude già presente, lettura da file")
            with open("relazione_finale.txt", "r") as f:
                relazione_finale = f.read()
        else:
            logging.info("🧠 Generazione relazione con Claude")
            output_gpt = None  # 🔐 Inizializza variabile

            if os.path.exists("output_gpt.txt"):
                with open("output_gpt.txt", "r") as f:
                    output_gpt = f.read()

            if not output_gpt:
                logging.error("❌ GPT non generato o vuoto, interrotto flusso Claude.")
                return JSONResponse(
                    content={"esito": "errore", "dettaglio": "output_gpt non disponibile"},
                    status_code=500
                )

            relazione_finale = genera_relazione_con_claude(output_gpt, bandi_compatibili)

            with open("relazione_finale.txt", "w") as f:
                f.write(relazione_finale)

            logging.info("✅ Relazione Claude completata e salvata")

        output_gpt = None

        if os.path.exists("output_gpt.txt"):
            logging.info("📄 Analisi GPT già presente, lettura da file")
            with open("output_gpt.txt", "r") as f:
                output_gpt = f.read()
        else:
            logging.info("🧠 Avvio analisi GPT")
            output_gpt = esegui_analisi_completa(path)

            with open("output_gpt.txt", "w") as f:
                f.write(output_gpt)

            logging.info("✅ Analisi GPT completata e salvata")

        return JSONResponse(content={
            "esito": "ok",
            "relazione": relazione_finale,
            "gpt": output_gpt
        })

    except Exception as e:
        logging.error(f"Errore durante l'elaborazione: {e}")
        return JSONResponse(content={"esito": "errore", "dettaglio": str(e)}, status_code=500)
