import os
from analisi_blocchi_gpt import analisi_completa_multipla
from claude_module import genera_relazione_con_claude
from email_handler import invia_email_con_make
from file_utils import estrai_testo_da_pdf, salva_output
from bandi_utils import carica_bandi

def esegui_analisi_completa(file_path, caratteristiche_impresa, csv_bandi_path):
    try:
        print("▶ Avvio estrazione dati dal bilancio PDF...")
        testo = estrai_testo_da_pdf(file_path)

        print("▶ Avvio caricamento bandi compatibili...")
        bandi = carica_bandi(csv_bandi_path)

        print("▶ Avvio analisi GPT a blocchi...")
        bilancio = testo
        visura = caratteristiche_impresa
        output_gpt = analisi_completa_multipla(bilancio, visura, bandi)
        salva_output("output_gpt.txt", output_gpt)

        print("▶ Avvio relazione finale con Claude...")
        relazione_finale = genera_relazione_con_claude(output_gpt, visura, bandi)
        salva_output("relazione_finale.txt", relazione_finale)

        print("▶ Invio relazione via email con Make...")
        invia_email_con_make(relazione_finale)

        print("✅ Analisi completata con successo.")
        return relazione_finale

    except Exception as e:
        errore = f"❌ Errore durante l'esecuzione dell'analisi: {e}"
        print(errore)
        return errore
