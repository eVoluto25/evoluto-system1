from estrazione_pdf import estrai_testo_da_pdf
from gpt_module import analisi_tecnica_gpt
from claude_module import genera_relazione_con_claude
from matching_bandi import carica_bandi, filtra_bandi_compatibili

def esegui_analisi_completa(file_path, caratteristiche_impresa, csv_bandi_path):
    testo = estrai_testo_da_pdf(file_path)
    output_gpt = analisi_tecnica_gpt(testo)
    bandi = carica_bandi(csv_bandi_path)
    bandi_compatibili = filtra_bandi_compatibili(bandi, caratteristiche_impresa)
    return genera_relazione_con_claude(output_gpt, "Preventivi", "Piano Ammortamento", bandi_compatibili)
