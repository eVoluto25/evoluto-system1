from estrazione_pdf import estrai_testo_da_pdf
from gpt_module import analisi_tecnica_gpt
from matching_bandi import carica_bandi, filtra_bandi_compatibili
from claude_module import genera_relazione_con_claude
from invio_email import invia_email_gmail
from pathlib import Path

def esegui_analisi_completa(file_path: Path, nome_azienda: str = "") -> str:
    # 1. Estrazione testo PDF
    testo = estrai_testo_da_pdf(file_path)
    if not testo:
        raise ValueError("❌ Il PDF non contiene testo valido.")

    # 2. Analisi tecnica GPT
    output_gpt = analisi_tecnica_gpt(testo)

    # 3. Dati simulati per preventivi e piano ammortamento
    preventivi = "Preventivo investimento: 45.000 € per macchinari"
    piano_ammortamento = "60 mesi – rata stimata 900 €/mese – TAN 1,8%"

    # 4. Caricamento bandi
    bandi = carica_bandi("bandi_tracker/bandi.csv")
    bandi_compatibili = filtra_bandi_compatibili(testo, bandi)

    # 5. Claude: relazione strategica finale
    relazione = genera_relazione_con_claude(
        output_gpt=output_gpt,
        preventivi=preventivi,
        piano_ammortamento=piano_ammortamento,
        bandi=bandi_compatibili
    )

    # 6. Salvataggio
    output_path = Path("output/relazione_finale.txt")
    with open(output_path, "w") as f:
        f.write(relazione)

    # 7. Invio email
    invia_email_gmail(
        destinatario="info@capitaleaziendale.it",
        oggetto=f"[CHECK] Verifica aziendale per {nome_azienda}",
        corpo_testo=f"Analisi ricevuta da {nome_azienda}. In allegato trovi la relazione completa.",
        allegato_path=output_path,
        email_mittente="verifica.evoluto@gmail.com",
        password_app="vvkj cybv njee qjts"  # già autorizzata
    )

    return relazione
