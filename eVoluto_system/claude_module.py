def prompt_claude(output_gpt, preventivi, piano_ammortamento, bandi):
    return f"""
Sintesi dell'analisi tecnica (GPT):
{output_gpt}

Ora integra queste informazioni e fornisci una visione strategica completa, strutturata nei seguenti punti:

1. Interpretazione tecnica sintetica e operativa del bilancio e della visura (in base ai dati ricevuti).

2. Analisi degli investimenti previsti:
   – Preventivi ricevuti:
{preventivi}
   – Piano di ammortamento stimato:
{piano_ammortamento}

3. Matching con le opportunità attualmente disponibili:
   – Esegui un confronto intelligente tra le caratteristiche dell’azienda e i seguenti bandi disponibili:
{bandi}

   – Per ciascun bando:
     • Verifica se è compatibile in base a:
       – Forma di agevolazione (es. fondo perduto, credito d’imposta, finanziamento agevolato)
       – Territorio di applicazione
       – Beneficiari ammessi
       – Finalità dell’incentivo
     • Indica il beneficio economico ottenibile e se l’intervento è cumulabile
     • Spiega il vantaggio competitivo per l’azienda

Obiettivo:
– Evidenzia le opportunità strategiche e concrete per rafforzare la solidità economica e finanziaria.
– Includi eventuali interventi correttivi, suggerimenti pratici e leve gestionali per migliorare margini, rating, fiscalità e accesso al credito.

Scrivi in modo chiaro, concreto, professionale e orientato all’azione. Niente teoria, solo ciò che serve all’imprenditore.
"""