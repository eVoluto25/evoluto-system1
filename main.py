import logging
from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import JSONResponse
from extractor import estrai_dati_da_pdf
from claude_module import genera_relazione_con_claude
from gpt_module import analisi_completa_multipla
from salva_output_html import salva_output_html
import shutil
import os

app = FastAPI()

@app.post("/analizza-pdf")
async def analizza_pdf(file: UploadFile, email: str = Form(...)):
    logging.info("
