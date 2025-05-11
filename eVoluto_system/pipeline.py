from estrazione_pdf import estrai_testo_da_pdf
from invio_email import invia_email_gmail
from pathlib import Path
from gpt_module import analisi_tecnica_gpt
from claude_module import genera_relazione_con_claude

def esegui_analisi_completa(file_path: Path, nome_azienda: str = "") -> str:
    testo = estrai_testo_da_pdf(file_path)

    if not testo:
        raise ValueError("❌ Il PDF non contiene testo valido.")

    # 1. Analisi tecnica GPT
    output_gpt = analisi_tecnica_gpt(testo, nome_azienda=nome_azienda)

    # 2. Recupera dati opzionali (es. preventivi, ammortamenti)
    preventivi = "Dato non disponibile"
    piano_ammortamento = "Dato non disponibile"

    # 3. Leggi i bandi disponibili (da CSV)
    with open("bandi_tracker/bandi.json", "r", encoding="utf-8") as f:
        bandi = f.read()

    # 4. Chiamata Claude per il matching e la strategia
    relazione_finale = genera_relazione_con_claude(
        output_gpt=output_gpt,
        preventivi=preventivi,
        piano_ammortamento=piano_ammortamento,
        bandi=bandi
    )

    # 5. Salvataggio output
    output_path = Path("output/relazione_finale.txt")
    with open(output_path, "w") as f:
        f.write(relazione_finale)

    # 6. Invio email
    invia_email_gmail(output_path)

    return relazione_finale
