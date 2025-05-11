from estrazione_pdf import estrai_testo_da_pdf
from invio_email import invia_email_gmail
from pathlib import Path
from pipeline import elabora_pipeline

def esegui_analisi_completa(file_path: Path, nome_azienda: str = "") -> str:
    testo = estrai_testo_da_pdf(file_path)

    if not testo:
        raise ValueError("❌ Il PDF non contiene testo valido.")

    relazione = elabora_pipeline(
        testo_pdf=testo,
        nome_azienda=nome_azienda,
        periodo="2023"
    )

    output_path = Path("output/relazione_finale.txt")
    with open(output_path, "w") as f:
        f.write(relazione)

    invia_email_gmail(
        destinatario="info@capitaleaziendale.it",
        oggetto=f"[CHECK] Verifica aziendale per {nome_azienda}",
        corpo_testo=f"Analisi ricevuta da {nome_azienda}. In allegato trovi la relazione completa.",
        allegato_path=output_path,
        email_mittente="verifica.evoluto@gmail.com",  
        password_app="vvkj cybv njee qjts"  
    )

    return relazione
