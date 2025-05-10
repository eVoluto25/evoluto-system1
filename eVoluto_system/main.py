import os
import json
from estrazione_pdf import estrai_testo_da_pdf
from gpt_module import analisi_tecnica_gpt
from claude_module import prompt_claude
from email_handler import recupera_email_con_allegati
from analisi_gpt import estrai_dati_documento

# DEBUG 1: Avvio
print("DEBUG 1: Avvio script")

# Carica i bandi dal file JSON aggiornato
try:
    with open("bandi_tracker/bandi_mimit.json", "r", encoding="utf-8") as f:
        bandi = json.load(f)
        print(f"DEBUG 2: Bandi caricati. Totale: {len(bandi)}")
except Exception as e:
    print("ERRORE nel caricamento dei bandi:", e)
    exit()

# Estrai il documento dall'ultima email ricevuta con allegato
try:
    documento_path = recupera_email_con_allegati()
    print(f"DEBUG 3: Documento scaricato: {documento_path}")
except Exception as e:
    print("ERRORE nel recupero del documento:", e)
    documento_path = None

# Verifica se è stato trovato un documento, altrimenti esce
if not documento_path:
    print("✘ Interruzione: nessun documento disponibile per analisi.")
    exit()

# Estrai i dati dal documento (bilancio, visura, ecc.)
try:
    dati = estrai_dati_documento(documento_path)
    print(f"DEBUG 4: Dati estratti:\n{dati}")
except Exception as e:
    print("ERRORE nell'estrazione dei dati:", e)
    dati = {}

# Prompt per GPT
try:
    output_gpt = analisi_tecnica_gpt(dati)
    print("DEBUG 5: Risposta GPT generata")
except Exception as e:
    print("ERRORE nel prompt GPT:", e)
    output_gpt = ""

# Prompt per Claude
try:
    output_claude = prompt_claude(
        output_gpt=output_gpt,
        preventivi=dati.get("preventivi", ""),
        piano_ammortamento=dati.get("ammortamento", "")
    )
    print("DEBUG 6: Risposta Claude generata")
except Exception as e:
    print("ERRORE nel prompt Claude:", e)
    output_claude = ""

# Salvataggio risultati
try:
    with open("output/output_gpt.txt", "w", encoding="utf-8") as f:
        f.write(output_gpt)
    with open("output/output_claude.txt", "w", encoding="utf-8") as f:
        f.write(output_claude)
    print("DEBUG 7: Output salvati")
except Exception as e:
    print("ERRORE nel salvataggio output:", e)