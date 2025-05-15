import logging
import openai
from indici_analisi import INDICI_REDDITIVITÀ, INDICI_SOLIDITÀ, INDICI_LIQUIDITÀ
from supabase_uploader import upload_html_to_supabase

import os
openai.api_key = os.getenv("OPENAI_API_KEY")

def suddividi_testo_in_blocchi(testo, max_token=1500):
    parole = testo.split()
    blocchi = []
    blocco_corrente = []

    for parola in parole:
        blocco_corrente.append(parola)
        if len(blocco_corrente) >= max_token:
            blocchi.append(" ".join(blocco_corrente))
            blocco_corrente = []

    if blocco_corrente:
        blocchi.append(" ".join(blocco_corrente))

    return blocchi
    
    def analizza_blocchi_gpt(testo_bilancio):
        blocchi = suddividi_testo_in_blocchi(testo_bilancio)
        risultati = []

    for i, blocco in enumerate(blocchi):
        logging.info(f"🔄 GPT – Elaborazione blocco {i+1}/{len(blocchi)}")
        try:
            risposta = analizza_completo_con_gpt(blocco)
            if risposta:
                risultati.append(risposta)
            else:
                logging.warning(f"⚠️ Blocco {i+1} – Nessuna risposta")
        except Exception as e:
            logging.error(f"❌ Errore durante l'elaborazione del blocco {i+1}: {e}")
    if risultati:
        return "\n\n".join(risultati)
    else:
        return None

def analizza_completo_con_gpt(testo_bilancio):
    logging.info("\U0001f916 Avvio analisi GPT completa con struttura indici...")

    # Organizzazione degli indici in sezioni strutturate
    prompt = f"""
Sei un analista finanziario. Analizza il seguente testo di bilancio, estraendo e commentando gli indici chiave per ciascuna area:

<h3>1. Redditività</h3>
<p>Indici da calcolare e interpretare:</p>
- {chr(10).join(['- ' + indice for indice in INDICI_REDDITIVITÀ])}

<h3>2. Solidità</h3>
<p>Indici da calcolare e interpretare:</p>
- {chr(10).join(['- ' + indice for indice in INDICI_SOLIDITÀ])}

<h3>3. Liquidità</h3>
<p>Indici da calcolare e interpretare:</p>
- {chr(10).join(['- ' + indice for indice in INDICI_LIQUIDITÀ])}

<h3>4. DSCR (Debt Service Coverage Ratio)</h3>
<p>Calcola il DSCR utilizzando i dati disponibili. Spiega cosa indica in termini di capacità di rimborso del debito. Concludi se il valore è positivo, neutro o critico.</p>

<h3>5. ESG stimato</h3>
<p>In base all’attività aziendale (settore ATECO), stima un valore medio ESG del settore e commenta se l’azienda potrebbe migliorare su ambiente, aspetti sociali o governance. Specifica che si tratta di una stima.</p>

<h3>6. Affidabilità bancaria (simulata)</h3>
<p>Sulla base dei dati di bilancio, fornisci un giudizio descrittivo (es. buono, borderline, critico) come farebbe una banca nel valutare l'affidabilità dell’impresa.</p>

<p>Analizza il testo seguente ed elabora un report ordinato, coerente e professionale. Concludi con un giudizio sintetico sulla sostenibilità economico-finanziaria dell’impresa.</p>

___
{testo_bilancio}
___
"""
   
    if risultati:
        return "\n\n".join(risultati)
    else:
        return None
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Sei un analista finanziario esperto di indici economico-finanziari."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4,
            max_tokens=2500
        )

        testo_output = response["choices"][0]["message"]["content"]
        logging.info("\U0001f4dc Report GPT generato correttamente.")
        return testo_output

    except Exception as e:
        logging.error(f"\u274c Errore durante la generazione del report GPT: {e}")
        return ""
