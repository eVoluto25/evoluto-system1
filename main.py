import logging
import os
from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import JSONResponse
from extractor import estrai_dati_da_pdf
from gpt_module import analizza_completo_con_gpt
from claude_module import genera_relazione_con_claude
from bandi_utils import aggiorna_bandi
from storage_handler import upload_html_to_supabase
from make_webhook import invia_a_make

app = FastAPI()

@app.api_route("/", methods=["GET", "HEAD"])
def root_head():
    return {"status": "✅ eVoluto backend attivo", "version": "1.0"}

@app.post("/analizza-pdf")
async def analizza_pdf(
    upload_1: UploadFile = Form(...),
    email_1: str = Form(...),
    telefono_1: str = Form(...),
    nome_1: str = Form(...)
):
    logging.info("✅ Ricevuto upload_1: %s, email_1: %s", upload_1.filename, email_1)

    temp_file_path = "temp_file.pdf"
    with open(temp_file_path, "wb") as f:
        f.write(await upload_1.read())

        logging.info("🚀 Inizio pipeline completa")

        caratteristiche_azienda, bilancio = estrai_dati_da_pdf(temp_file_path)
        logging.info("📄 Estrazione dati completata")

        logging.info(f"🧾 Caratteristiche azienda: {caratteristiche_azienda}")
        logging.info(f"📊 Estratto bilancio: primi 200 caratteri → {bilancio[:200]}")

        if not caratteristiche_azienda or not bilancio or bilancio.strip() == "":
            logging.warning("⚠️ Dati aziendali o bilancio assenti, interruzione pipeline.")
            return JSONResponse(status_code=422,content={"errore": "Dati insufficienti", "caratteristiche": caratteristiche_azienda, "bilancio": bilancio}
    )

        logging.info("🤖 Chiamata a GPT in corso...")
        analisi_finanziaria = analizza_completo_con_gpt(bilancio, caratteristiche_azienda)
        html_finale = f"<html><body>{analisi_finanziaria}</body></html>"
        link_gpt = upload_html_to_supabase(html_finale, "output_gpt.html")
        
        if not analisi_finanziaria or analisi_finanziaria.strip() == "":
            logging.error("❌ GPT ha restituito una risposta vuota o nulla.")
            return JSONResponse(status_code=422, content={"errore": "Analisi GPT non riuscita"})

        logging.info("📡 Aggiornamento bandi pubblici in corso")
        bandi_compatibili = aggiorna_bandi()

        logging.info("📎 Generazione relazione finale tramite Claude")
        relazione_finale = genera_relazione_con_claude(analisi_finanziaria, caratteristiche_azienda, bandi_compatibili)

        html_claude = f"<html><body>{relazione_finale}</body></html>"
        link_claude = upload_html_to_supabase(html_claude, "output_claude.html")

        try:
            payload = {
            "denominazione": caratteristiche_azienda.get("denominazione", "N/D"),
            "amministratore": caratteristiche_azienda.get("amministratore", "N/D"),
            "outputGpt": link_gpt,
            "outputClaude": link_claude
        }
            
    from supabase_client import supabase  # già pronto nel tuo progetto
    try:
        invia_a_make(payload)
            logging.info("✅ Pipeline completata con successo, Make riceve link HTML")
        
         # 🔽 Inserimento in Supabase per Make
         supabase.table("analisi_gpt").insert({
             "email": email_1,
             "telefono": telefono_1,
             "nome": nome_1,
             "output_gpt": link_gpt,
             "output_claude": link_claude
             "denominazione": caratteristiche_azienda.get("denominazione", "N/D"),
             "amministratore": caratteristiche_azienda.get("amministratore", "N/D"),
             "inviato": False
         }).execute()
         logging.info("📩 Link salvati su Supabase per invio Make")
            "status": "ok",
            "outputGpt": link_gpt,
            "outputClaude": link_claude
            "inviato": False
        }
        
        except Exception as e:
            logging.warning(f"❌ Errore durante l'invio a Make: {e}")
            # Provo a rimuovere il file temporaneo
            try:
                os.remove(temp_file_path)
                logging.info("🧹 File temporaneo rimosso con successo.")
        except Exception as e:
            logging.warning(f"⚠️ Errore durante la rimozione del file temporaneo: {e}")
        return {
            "analisi": analisi_finanziaria,
            "bandi": bandi_compatibili,
            "relazione_finale": genera_relazione_con_claude(
                analisi_finanziaria, caratteristiche_azienda, bandi_compatibili
            )
        }  
