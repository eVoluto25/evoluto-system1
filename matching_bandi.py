import json
import logging

def confronta_con_bandi(caratteristiche_azienda):
    try:
        with open("bandi_bandi.json", "r", encoding="utf-8") as f:
            bandi = json.load(f)
    except Exception as e:
        logging.error(f"Errore apertura bandi: {e}")
        return []

    forma = caratteristiche_azienda.get("forma_giuridica", "").lower()
    ateco = caratteristiche_azienda.get("codice_ateco", "").split(".")[0]
    attivita = caratteristiche_azienda.get("attivita_prevalente", "").lower()

    bandi_compatibili = []

    for bando in bandi:
        beneficiari = bando.get("beneficiari", "").lower()
        settori = bando.get("settori", "").lower()
        ateco_bando = bando.get("ateco", "")

        if (
            forma in beneficiari
            or any(k in settori for k in [forma, attivita])
            or (ateco and ateco in ateco_bando)
        ):
            bandi_compatibili.append(bando)

    logging.info(f"Bandi compatibili trovati: {len(bandi_compatibili)}")
    return bandi_compatibili
