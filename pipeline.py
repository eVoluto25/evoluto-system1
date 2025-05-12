from pathlib import Path
from estrazione_pdf import estrai_testo_da_pdf
from gpt_module import analisi_tecnica_gpt
from matching_bandi import esegui_matching
from claude_module import genera_relazione_con_claude
from invio_email import invia_email_gmail

def elabora_pipeline(testo_pdf: str, nome_azienda: str = "Impresa S.r.l."):
    print("▶️ Avvio elaborazione GPT...")
    output_gpt = analisi_tecnica_gpt(testo_pdf)

    print("▶️ Esecuzione matching bandi...")
    bandi = esegui_matching(testo_pdf)

    # Simulazione input opzionali
    preventivi = "Preventivo: software gestionale €12.000, macchinari €25.000"
    piano_ammortamento = "Piano: 36 mesi, rata 1.100€/mese, tasso 1,5%"

    print("▶️ Generazione relazione finale con Claude...")
    relazione = genera_relazione_con_claude(
        output_gpt=output_gpt,
        preventivi=preventivi,
        piano_ammortamento=piano_ammortamento,
        bandi=bandi
    )

    print("✅ Relazione generata correttamente.")
    return relazione

def esegui_analisi_completa(file_path: Path, nome_azienda: str = "Impresa S.r.l.") -> str:
    print(f"📄 Lettura file: {file_path}")
    testo = estrai_testo_da_pdf(file_path)

    if not testo:
        raise ValueError("❌ Il file PDF non contiene testo valido.")

    relazione = elabora_pipeline(testo_pdf=testo, nome_azienda=nome_azienda)

    output_path = Path("output/relazione_finale.txt")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        f.write(relazione)

    invia_email_gmail(
        destinatario="info@capitaleaziendale.it",
        oggetto=f"[CHECK] Verifica aziendale per {nome_azienda}",
        corpo_testo=f"Analisi completata per {nome_azienda}. In allegato trovi la relazione completa.",
        allegato_path=output_path,
        email_mittente="verifica.evoluto@gmail.com",
        password_app="vvkj cybv njee qjts"
    )

    return relazione
