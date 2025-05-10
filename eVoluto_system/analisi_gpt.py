import os
from estrazione_pdf import estrai_testo_da_pdf

PDF_DIR = "estratti_pdf"

def estrai_dati_documento(documento_path):
    nome_file = os.path.basename(documento_path)
    with open(documento_path, "rb") as f:
        testo = estrai_testo_da_pdf(f.read())

    # Simulazione di parsing da testo
    dati = {
        "bilancio": testo,
        "visura": "Contenuto visura simulato",
        "preventivi": "Preventivo 1: 30.000 €",
        "ammortamento": "5 anni"
    }

    # Salvataggio in estratti_pdf/
    os.makedirs(PDF_DIR, exist_ok=True)
    estratto_path = os.path.join(PDF_DIR, nome_file.replace(".pdf", ".txt"))
    with open(estratto_path, "w", encoding="utf-8") as f:
        f.write(testo)

    return dati