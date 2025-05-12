import pandas as pd
from config import BANDI_CSV_PATH

def normalizza_testo(testo):
    if not isinstance(testo, str):
        return ""
    return testo.lower().strip()

def verifica_compatibilita_bando(bando, caratteristiche_azienda):
    """
    Confronta le caratteristiche dell’azienda con i requisiti del bando.
    """
    try:
        for campo in ["territorio", "beneficiari", "settore", "forma_agevolazione", "finalita"]:
            valore_bando = normalizza_testo(bando.get(campo, ""))
            valore_azienda = normalizza_testo(caratteristiche_azienda.get(campo, ""))
            if valore_azienda and valore_azienda not in valore_bando:
                return False
        return True
    except Exception as e:
        print(f"Errore nella verifica compatibilità: {e}")
        return False

def filtra_bandi_compatibili(caratteristiche_azienda):
    """
    Restituisce un elenco di bandi compatibili con l'azienda analizzata.
    """
    try:
        df = pd.read_csv(BANDI_CSV_PATH)
        bandi_compatibili = []

        for _, bando in df.iterrows():
            if verifica_compatibilita_bando(bando, caratteristiche_azienda):
                bandi_compatibili.append({
                    "titolo": bando.get("titolo", ""),
                    "link": bando.get("link", ""),
                    "contributo": bando.get("forma_agevolazione", ""),
                    "finalita": bando.get("finalita", "")
                })

        return bandi_compatibili

    except FileNotFoundError:
        return [{"errore": "⚠️ File bandi non trovato."}]
    except Exception as e:
        return [{"errore": f"⚠️ Errore imprevisto: {e}"}]
