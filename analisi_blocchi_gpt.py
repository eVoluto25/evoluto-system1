import os
import logging
from gpt_module import analisi_completa_multipla
from email_handler import invia_email

# Funzione per dividere il testo in blocchi
def dividi_blocchi(testo: str, max_caratteri: int = 10000) -> list:
    return [testo[i:i + max_caratteri] for i in range(0, len(testo), max_caratteri)]

# Funzione principale
def analisi_completa_multipla(testo):
    blocchi = dividi_blocchi(testo)
    risultati = []

    for i, blocco in enumerate(blocchi):
        path_blocco = f"blocco_{i+1}.txt"

        # Check se esiste già il file salvato
        if os.path.exists(path_blocco):
            try:
                with open(path_blocco, "r") as f:
                    risultati.append(f.read())
                continue
            except Exception as e:
                logging.warning(f"⚠️ Errore lettura blocco salvato {i+1}: {e}")

        # Analisi GPT del blocco
        try:
            logging.info(f"📤 GPT – Invio blocco {i+1} di {len(blocchi)}")
            risposta = analisi_tecnica_gpt(blocco)

            if not risposta or len(risposta.strip()) < 10:
                raise ValueError("Risposta GPT troppo corta o vuota")

            risultati.append(risposta)

            # Salvataggio file
            with open(path_blocco, "w") as f:
                f.write(risposta)

        except Exception as e:
            logging.error(f"❌ Errore nel blocco {i+1}: {e}")
            risultati.append(f"[ERRORE BLOCCO {i+1}] GPT non ha fornito una risposta valida.")
            continue

    return "\n\n".join(risultati)
