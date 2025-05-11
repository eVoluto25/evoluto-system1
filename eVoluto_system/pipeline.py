from estrazione_pdf import estrai_testo_da_pdf
from invio_email import invia_email_gmail
from pathlib import Path
from pipeline import elabora_pipeline  # Assicurati che il modulo non richieda più 'periodo'

def esegui_analisi_completa(file_path: Path, nome_azienda: str = "") -> str:
    # Estrai il testo dal PDF
    testo = estrai_testo_da_pdf(file_path)

    if not testo:
        raise ValueError("❌ Il PDF non contiene testo valido.")

    # Esegui la pipeline di analisi (senza parametro 'periodo')
    relazione = elabora_pipeline(
        testo_pdf=testo,
        nome_azienda=nome_azienda
    )

    # Salva il risultato nel file
    output_path = Path("output/relazione_finale.txt")
    with open(output_path, "w") as f:
        f.write(relazione)

    # Invia l'output finale per email
    invia_email_gmail(output_path)

    return relazione
