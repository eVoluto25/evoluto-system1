import openai
import logging

openai.api_key = os.getenv("OPENAI_API_KEY")

def analizza_completo_con_gpt(contenuto_pdf: str) -> str:
    try:
        logging.info("🤖 Chiamata a GPT-3.5 in corso...")

        prompt = (
            "Agisci come un analista esperto di bilanci aziendali."
            " Ricevi di seguito il contenuto di un documento PDF estratto da una Visura Camerale e dal Bilancio."
            " Il tuo compito è analizzare i dati e sintetizzare eventuali criticità, anomalie o spunti utili."
            " Non limitarti a descrivere: evidenzia ciò che potrebbe destare attenzione o preoccupazione per un consulente o un investitore."
            "\n\n---\n\n"
            f"{contenuto_pdf}"
            "\n\n---\n\n"
            "Rispondi con un'analisi completa, divisa in paragrafi chiari con titoli."
        )

        risposta = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=3900,
        )

        contenuto = risposta.choices[0].message.content
        logging.info("✅ GPT ha restituito una risposta valida.")
        return contenuto

    except Exception as e:
        logging.error(f"❌ Errore durante l'elaborazione con GPT: {e}")
        return "[ERRORE GPT]"
