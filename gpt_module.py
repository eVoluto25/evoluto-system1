import logging
import openai
import os
from storage_handler import upload_html_to_supabase

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

def genera_prompt_bancabile(testo_estratto):
    prompt = f"""
Sei un CFO esperto in analisi bancarie. Ricevi un bilancio aziendale e devi fornire una valutazione tecnica, sintetica e leggibile da un direttore bancario. 
📌 Dati aziendali:
- Denominazione: {caratteristiche.get('denominazione', 'N/D')}
- Codice ATECO: {caratteristiche.get('codice_ateco', 'N/D')}
- CAP: {caratteristiche.get('cap', 'N/D')}
- Provincia: {caratteristiche.get('provincia', 'N/D')}

Per ciascun indice, calcola il valore numerico e affianca un giudizio sintetico (🔵 Ottimo / 🟢 Buono / 🟡 Sufficiente / 🟠 Debole / 🔴 Critico). Non scrivere spiegazioni testuali.

<h4>1. Redditività</h4>
<ul>
  <li>ROE</li>
  <li>ROI</li>
  <li>ROS</li>
  <li>EBITDA margin</li>
  <li>Net Profit Margin</li>
</ul>

<h4>2. Solidità patrimoniale</h4>
<ul>
  <li>Equity Ratio</li>
  <li>Indice di indipendenza finanziaria</li>
  <li>Indice di copertura immobilizzazioni</li>
  <li>Leverage</li>
</ul>

<h4>3. Liquidità e flussi</h4>
<ul>
  <li>Current Ratio</li>
  <li>Quick Ratio</li>
  <li>Cash Ratio</li>
  <li>Cash Flow / Debiti</li>
  <li>DSCR (stimato)</li>
</ul>

<h4>4. Compatibilità gestionale</h4>
<p>Analizza la coerenza tra il codice ATECO, la forma giuridica e i principali dati economici. Segnala eventuali incongruenze o criticità nel modello di business.</p>

<h4>5. Simulazione sostenibilità nuovi debiti (60 mesi)</h4>
<p>Valuta se l’impresa può sostenere un nuovo impegno finanziario nei seguenti 3 scenari:</p>
<ul>
  <li>Prestito da €50.000</li>
  <li>Prestito da €100.000</li>
  <li>Prestito da €150.000</li>
</ul>
<p>Per ogni scenario, indica: sostenibilità prevista, rapporto rata/debito, eventuali condizioni da rispettare.</p>

<h4>6. Voto di affidabilità bancaria</h4>
<p>Esprimi un voto finale sintetico da CFO destinato a un comitato crediti. Usa una scala A – B – C – D – E con motivazione tecnica stringata.</p>

<h4>7. Valutazione Sostenibilità ed ESG</h4>
<p>Valuta, sulla base del settore di appartenenza (codice ATECO) e delle informazioni disponibili nel bilancio, il livello di sostenibilità ESG (ambientale, sociale, governance).</p>
<p>Se i dati non sono sufficienti, esegui una stima basata sul settore e sulla forma giuridica dell’impresa.</p>
<p>Esprimi il giudizio finale con una scala sintetica: 🔵 Alto – 🟢 Buono – 🟡 Medio – 🟠 Basso – 🔴 Critico</p>

<h4>Formato</h4>
<p>Restituisci la risposta in formato HTML, usa &lt;ul&gt; per le liste e &lt;h4&gt; per i blocchi. Nessun commento narrativo: solo dati e valutazioni sintetiche. Ogni indice deve avere accanto il voto.</p>

Dati del bilancio:
{text_estratto}
"""
    return prompt

def analizza_completo_con_gpt(testo):
    prompt = genera_prompt_bancabile(testo)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Sei un analista finanziario esperto."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4,
        max_tokens=3000
    )
    return response.choices[0].message["content"].strip()

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
        html_finale = "<html><body>" + "<hr>".join(risultati) + "</body></html>"
        url_output = upload_html_to_supabase(html_finale, filename_prefix="output_gpt")
        return url_output
    else:
        return None
