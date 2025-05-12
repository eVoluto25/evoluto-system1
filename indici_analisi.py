# indici_analisi.py

# ✅ Indici di Redditività
INDICI_REDDITIVITÀ = [
    "ROE (Return on Equity): Risultato Netto / Patrimonio Netto",
    "ROI (Return on Investment): Risultato Operativo / Capitale Investito Netto Operativo",
    "ROS (Return on Sales): Risultato Operativo / Vendite",
    "ROT (Return on Turnover): Vendite / Capitale Investito Netto Operativo",
    "ROIC (Return on Invested Capital): Nopat / Capitale Investito Netto Operativo (media ultimi 2 anni)"
]

# ✅ Indici di Solidità
INDICI_SOLIDITÀ = [
    "Copertura Immobilizzazioni: (Patrimonio Netto + Passività a lungo) / Attivo Immobilizzato",
    "Indipendenza Finanziaria: Patrimonio Netto / Totale Attivo",
    "Leverage: Totale Attivo / Patrimonio Netto",
    "PFN/PN (Posizione Finanziaria Netta / Patrimonio Netto)"
]

# ✅ Indici di Liquidità
INDICI_LIQUIDITÀ = [
    "Current Ratio: Attività a breve / Passività a breve",
    "Quick Ratio: (Attività a breve - Rimanenze) / Passività a breve",
    "Margine di Tesoreria: Attività liquide / Passività correnti",
    "Margine di Struttura: Patrimonio Netto / Totale Attivo",
    "Capitale Circolante Netto: Attività a breve - Passività a breve"
]

# ✅ Indici di Copertura Finanziaria
INDICI_COPERTURA = [
    "EBIT/OF: Risultato Operativo / Oneri Finanziari",
    "MOL/PFN: Margine Operativo Lordo / Posizione Finanziaria Netta",
    "Flusso di Cassa / OF: Flusso di Cassa operativo / Oneri Finanziari",
    "PFN/MOL: Posizione Finanziaria Netta / Margine Operativo Lordo",
    "PFN/Ricavi: Posizione Finanziaria Netta / Ricavi"
]

# ✅ Indici di Rischio e Credito
INDICI_RISCHIO_CREDITO = [
    "Cash Wallet Risk Index",
    "Collateral Distortion Index",
    "Sconfinamento Medio",
    "Tensione Finanziaria"
]

# ✅ Altri Indici
INDICI_ALTRI = [
    "Cash Wallet Management Index",
    "Duration",
    "Punteggio MCC (Merit Credit Score)"
]

# ✅ Funzione per ottenere tutti gli indici raggruppati
def get_tutti_gli_indici():
    return {
        "redditività": INDICI_REDDITIVITÀ,
        "solidità": INDICI_SOLIDITÀ,
        "liquidità": INDICI_LIQUIDITÀ,
        "copertura finanziaria": INDICI_COPERTURA,
        "rischio e credito": INDICI_RISCHIO_CREDITO,
        "altri": INDICI_ALTRI
    }
