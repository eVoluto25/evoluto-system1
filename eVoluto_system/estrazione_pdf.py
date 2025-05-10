import fitz  # PyMuPDF
import os

def estrai_testo_da_pdf(percorso_file):
    try:
        if not percorso_file or not os.path.isfile(percorso_file):
            print("⚠️ File PDF non valido o inesistente.")
            return None

        doc = fitz.open(percorso_file)
        testo = ""

        for pagina in doc:
            testo += pagina.get_text()

        doc.close()

        if not testo.strip():
            print("⚠️ Il contenuto del PDF è vuoto.")
            return None

        return testo.strip()

    except Exception as e:
        print(f"ERRORE durante l'estrazione del PDF: {e}")
        return None