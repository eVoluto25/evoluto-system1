def prompt_gpt(bilancio, visura, bandi):
    return f"""
Sei un CFO esperto in analisi economico-finanziaria, merito creditizio e continuità aziendale.

Hai ricevuto i seguenti documenti:
- Bilancio d'esercizio:
{bilancio}

- Visura camerale:
{visura}

- Elenco dei bandi disponibili:
{bandi}

Analizza i dati fornendo una valutazione tecnica completa e sintetica, strutturata nei seguenti ambiti:

Analisi di bilancio e performance aziendale
• Riclassificazione del bilancio e analisi dell’indebitamento
• 40 indici di bilancio commentati e valutazione della performance
• Rendiconto finanziario secondo principi IAS e OIC
• Analisi economico-finanziaria
• Analisi della Posizione Finanziaria Netta

Analisi del merito creditizio e della Centrale Rischi
• Score merito creditizio stimato
• Analisi della Centrale Rischi (mensile e annuale)
• Anomalie sulle singole linee di credito
• Analisi andamentale (ultimo mese, ultimi 12 mesi, intero rapporto)
• Screening bancario: Sofferenze, crediti scaduti, impagati, deteriorati
• Garanzie ricevute, crediti di firma, derivati, enti segnalanti
• Criticità gestionali e suggerimenti per migliorare il merito creditizio

Rating e valutazione del rischio
• Rating MCC, S&P, Indice di Altman
• Calcolo del rating con algoritmo proprietario
• Interventi per il miglioramento del rating

Indicatori della crisi e conformità normativa
• Indicatori della crisi elaborati dal CNDCEC
• Rendiconto finanziario e analisi della crisi d’impresa
• Giudizio sulla conformità al Codice della Crisi
• Valutazione della continuità aziendale
• Report Crisi d’Impresa

Analisi di compatibilità con i bandi di finanziamento
• Verifica della corrispondenza tra i requisiti dei bandi e le caratteristiche dell'impresa (es. codici ATECO, dimensione, sede operativa)
• Valutazione della coerenza tra gli obiettivi dei bandi e i progetti aziendali
• Identificazione dei bandi più adatti e suggerimenti per la candidatura

Scrivi in modo tecnico, professionale, utile all’imprenditore.
"""
   