import logging
from env_loader import carica_variabili_ambiente
from output_uploader import salva_output_html
import anthropic

def analizza_con_claude(caratteristiche_azienda, analisi_gpt, bandi_compatibili):
    config = carica_variabili_ambiente()
    client = anthropic.Anthropic(api_key=config["ANTHROPIC_API_KEY"])

    prompt = crea_prompt_claude(caratteristiche_azienda, analisi_gpt, bandi_compatibili)

    try:
        response = client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1800,
            temperature=0.3,
            system="Sei un esperto di finanza agevolata e analisi aziendale. Confronta i bandi con l'azienda.",
            messages=[{"role": "user", "content": prompt}]
        )

        contenuto = response.content[0].text
        if not contenuto.strip():
            raise ValueError("Claude ha restituito una risposta vuota")

        return contenuto

    except Exception as e:
        logging.error(f"Errore Claude: {e}")
        return "Errore nella generazione della risposta Claude."

def crea_prompt_claude(azienda, analisi, bandi):
    intestazione = f"""L'azienda analizzata ha le seguenti caratteristiche:
- Forma giuridica: {azienda.get('forma_giuridica')}
- Codice ATECO: {azienda.get('codice_ateco')}
- Attività: {azienda.get('attivita_prevalente')}

Analisi GPT:
{analisi}

Bandi compatibili filtrati:
""" + "\n".join([f"- {b['titolo']} ({b.get('forma_agevolazione', '')})" for b in bandi[:10]])

    chiusura = "\n\nFornisci una sintesi utile e personalizzata per l'imprenditore."

    return intestazione + chiusura
