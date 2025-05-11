# claude_analisi.py

from indici_analisi import get_tutti_gli_indici

def analizza_con_claude(testo_estratto: str, dati_bilancio: dict = None, bando: str = "", preventivi: str = "", piano_ammortamento: str = "") -> str:
    indici = get_tutti_gli_indici()

    prompt = f"""
Sei un analista finanziario esperto in finanza d'impresa e accesso a fondi pubblici.
Riceverai il testo di un bilancio aziendale o dati già strutturati, un bando pubblico, e documentazione economica da valutare.

🎯 Obiettivo:
1. Analizza la redditività, solidità, liquidità, copertura finanziaria e rischi.
2. Verifica se l'azienda può partecipare al bando.
3. Valuta se le spese previste sono ammissibili.
4. Commenta la sostenibilità finanziaria e i vantaggi ottenibili.

📄 Dati di input:
Testo bilancio:
{testo_estratto}

Indici da utilizzare:
- Redditività: {", ".join(indici["redditività"])}
- Solidità: {", ".join(indici["solidità"])}
- Liquidità: {", ".join(indici["liquidità"])}
- Copertura finanziaria: {", ".join(indici["copertura finanziaria"])}
- Rischi e credito: {", ".join(indici["rischio e credito"])}
- Altri: {", ".join(indici["altri"])}

Bando attivo:
{bando if bando else "Nessun bando indicato."}

Preventivi:
{preventivi if preventivi else "Nessun preventivo ricevuto."}

Piano di ammortamento:
{piano_ammortamento if piano_ammortamento else "Non disponibile."}

📌 Output atteso:
Restituisci un'analisi chiara e tecnica, utile per il matching bandi.
"""
    return prompt
