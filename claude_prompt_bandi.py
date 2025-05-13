import os
from anthropic import Anthropic

# Inizializza il client Claude in modo sicuro
API_KEY = os.getenv("ANTHROPIC_API_KEY")
if not API_KEY:
    raise ValueError("❌ Variabile d'ambiente 'ANTHROPIC_API_KEY' non trovata."
                     " Assicurati di averla configurata nel tuo ambiente.")

client = Anthropic(api_key=API_KEY)

# Prompt base con variabili da riempire
PROMPT_BASE = """
Agisci come analista finanziario esperto in bandi pubblici. Ricevi un elenco di bandi compatibili con l'impresa e devi scrivere una sezione di relazione destinata all'imprenditore.

Utilizza uno stile chiaro, rassicurante e focalizzato sul vantaggio concreto per l’azienda. Trasforma ogni bando in un'opportunità strategica.

Azienda: {forma} / Settore: {ateco} / Regione: {regione} / Dimensione: {dimensione}

Bandi compatibili:
{elenco_bandi}
"""

def genera_paragrafo_bandi_claude(azienda: dict, bandi: list) -> str:
    """
    Genera un testo descrittivo dei bandi compatibili tramite Claude.

    :param azienda: dict con chiavi "forma_giuridica", "codice_ateco", "regione", "dimensione_impresa"
    :param bandi: lista di dizionari con i dati dei bandi filtrati
    :return: stringa generata da Claude
    """
    elenco = ""
    for i, b in enumerate(bandi, 1):
        elenco += (
            f"{i}. Titolo: \"{b.get('Titolo', 'Sconosciuto')}\"\n"
            f"   Forma agevolazione: {b.get('Forma_agevolazione', 'N/A')}\n"
            f"   Scadenza: {b.get('Scadenza', 'N/A')}\n"
            f"   Ente: {b.get('Ente', 'N/A')}\n\n"
        )

    prompt = PROMPT_BASE.format(
        forma=azienda.get("forma_giuridica", "SRL").upper(),
        ateco=azienda.get("codice_ateco", "00.00"),
        regione=azienda.get("regione", ""),
        dimensione=azienda.get("dimensione_impresa", ""),
        elenco_bandi=elenco.strip()
    )

    response = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=1000,
        temperature=0.4,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.content[0].text if response.content else ""
