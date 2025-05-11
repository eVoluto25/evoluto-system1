from estrazione_pdf import estrai_testo_da_pdf

def esegui_analisi_completa(file_path: Path, nome_azienda: str = "") -> str:
    testo = estrai_testo_da_pdf(file_path)

    if not testo:
        raise ValueError("Il PDF non contiene testo valido")

    risultato = elabora_pipeline(
        testo_pdf=testo,
        nome_azienda=nome_azienda,
        periodo="2023"  # oppure auto-calcolato con datetime
    )

    output_path = Path("output") / "relazione_finale.txt"
    with open(output_path, "w") as f:
        f.write(risultato)

    return risultato
