def calcola_indici_bilancio(dati):
    ricavi = dati.get("ricavi", 0)
    utile = dati.get("utile", 0)
    ebit = dati.get("ebit", 0)
    ebitda = dati.get("ebitda", 0)
    patrimonio = dati.get("patrimonio", 1)
    attivo_totale = dati.get("attivo_totale", 1)
    passivo_corrente = dati.get("passivo_corrente", 1)
    attivo_corrente = dati.get("attivo_corrente", 1)
    liquidita = dati.get("liquidita", 0)
    debiti = dati.get("debiti", 1)
    debiti_bancari = dati.get("debiti_bancari", 0)
    oneri_finanziari = dati.get("oneri_finanziari", 1)
    ammortamenti = dati.get("ammortamenti", 0)
    ccn = dati.get("variazione_ccn", 0)
    pf_netta = dati.get("pf_netta", 1)
    rata_debito = dati.get("rata_debito", 1)
    indici = {
        "ROE": utile / patrimonio,
        "ROI": ebit / attivo_totale,
        "ROS": ebit / ricavi,
        "EBITDA Margin": ebitda / ricavi,
        "Utile su Ricavi": utile / ricavi,
        "Oneri Finanziari su Ricavi": oneri_finanziari / ricavi,
        "Indice di Indebitamento": debiti / patrimonio,
        "Debt/Equity": pf_netta / patrimonio,
        "Current Ratio": attivo_corrente / passivo_corrente,
        "Quick Ratio": (attivo_corrente - dati.get("magazzino", 0)) / passivo_corrente,
        "Margine di Tesoreria": liquidita / passivo_corrente,
        "DSCR": (utile + ammortamenti + ccn) / rata_debito,
        "PFN/EBITDA": pf_netta / ebitda,
        "Copertura Interessi (EBIT/Oneri)": ebit / oneri_finanziari
    }
    return {k: round(v, 2) if isinstance(v, (int, float)) else "n/d" for k, v in indici.items()}
