import logging
logging.basicConfig(level=logging.INFO)
from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import JSONResponse
from pathlib import Path
from datetime import datetime
import os

from pipeline import esegui_analisi_completa

app = FastAPI()

@app.api_route("/", methods=["GET", "HEAD"])
async def root():
    return {"status": "ok"}
    
@app.post("/analizza-pdf")
async def analizza_pdf(
    name: str = Form(..., alias="name_2"),
    phone: str = Form(..., alias="phone_1"),
    email: str = Form(..., alias="email_1"),
    upload: UploadFile = Form(..., alias="upload_1")
):
    try:
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"{timestamp}_{upload.filename}"
        upload_folder = Path("uploads")
        upload_folder.mkdir(exist_ok=True)
        Path("uploads").mkdir(parents=True, exist_ok=True)
        path = Path("uploads") / filename
        with open(path, "wb") as f:
            f.write(await upload.read())
        logging.info(f"🟢 RICEVUTA: {name}, {phone}, {email}, file={upload.filename}")

# 🧾 Check se esiste già la relazione Claude salvata
if os.path.exists("relazione_finale.txt"):
    logging.info("📄 Relazione Claude già presente, lettura da file")
    with open("relazione_finale.txt", "r") as f:
        relazione_finale = f.read()
else:
    logging.info("🧠 Generazione relazione con Claude")
    relazione_finale = genera_relazione_con_claude(output_gpt, bandi_compatibili)
    with open("relazione_finale.txt", "w") as f:
        f.write(relazione_finale)
    logging.info("✅ Relazione Claude completata e salvata")
        
        logging.info("🧠 Avvio esecuzione completa: GPT + Claude")
        # 📁 Check se esiste già l'output GPT salvato
if os.path.exists("output_gpt.txt"):
    logging.info("📁 Analisi GPT già presente, lettura da file")
    with open("output_gpt.txt", "r") as f:
        output_gpt = f.read()
else:
    logging.info("🧠 Avvio analisi GPT")
    output_gpt = analisi_completa_multipla(path)  # path al PDF o testo
    with open("output_gpt.txt", "w") as f:
        f.write(output_gpt)
    logging.info("✅ Analisi GPT completata e salvata")
        esegui_analisi_completa(path, {"nome": name, "email": email, "telefono": phone}, "dataset_bandi.csv")
        logging.info("✅ Esecuzione completa terminata.")
        return JSONResponse(content={"esito": "ok"})
    except Exception as e:
        logging.error(f"Errore durante l'elaborazione: {e}")
        return JSONResponse(content={"esito": "errore", "dettaglio": str(e)}, status_code=500)
