import pandas as pd
from pathlib import Path
from claude_module import verifica_compatibilita_bando  # funzione da definire

def matching_bandi_con_azienda(percorso_csv, testo_azienda):
    risultati = []

    # Carica i bandi dal CSV
    df = pd.read_csv(percorso_csv)
    
    for index, row in df.iterrows():
        titolo = row.get("titolo", "")
        descrizione = row.get("descrizione", "")
        regione = row.get("territorio", "")
        forma = row.get("forma_agevolazione", "")
        beneficiari = row.get("beneficiari", "")
        
        # Combina i dati del bando in un testo coerente
        testo_bando = f"TITOLO: {titolo}\nDESCRIZIONE: {descrizione}\nREGIONE: {regione}\nFORMA AGEVOLAZIONE: {forma}\nBENEFICIARI: {beneficiari}"
        
        try:
            # Chiamata al modello Claude o GPT per la verifica
            esito = verifica_compatibilita_bando(testo_azienda, testo_bando)
            risultati.append({
                "bando": titolo,
                "compatibile": esito.get("compatibile", False),
                "motivo": esito.get("motivo", "N/D"),
                "contributo": esito.get("contributo", "N/D"),
                "probabilita": esito.get("probabilita", "N/D")
            })
        except Exception as e:
            risultati.append({
                "bando": titolo,
                "compatibile": False,
                "motivo": f"Errore durante l’analisi: {str(e)}",
                "contributo": "N/D",
                "probabilita": "N/D"
            })

    return risultati
