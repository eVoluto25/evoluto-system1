import os
from gpt_module import analisi_tecnica_gpt  # Funzione che chiama GPT

# ✅ Funzione per dividere il testo in blocchi
def dividi_blocchi(testo: str, max_caratteri: int = 10000) -> list:
    """
    Divide il testo in blocchi da massimo `max_caratteri` caratteri.
    Utile per evitare problemi di lunghezza input nei modelli GPT.
    """
    return [testo[i:i + max_caratteri] for i in range(0, len(testo), max_caratteri)]

# ✅ Funzione principale che esegue l’analisi su più blocchi
def analisi_completa_multipla(testo):
    blocchi = dividi_blocchi(testo)
    risultati = []

    for i, blocco in enumerate(blocchi):
        path_blocco = f"blocco_{i+1}.txt"

        # Salta i blocchi già analizzati
        if os.path.exists(path_blocco):
            with open(path_blocco, "r") as f:
                risultati.append(f.read())
            continue

        # Chiamata a GPT sul blocco
        try:
            risposta = analisi_tecnica_gpt(blocco, "", "")  # visura e bandi possono essere vuoti
            risultati.append(risposta)

            with open(path_blocco, "w") as f:
                f.write(risposta)

        except Exception as e:
            print(f"Errore nel blocco {i+1}:", e)
            break

    return "\n\n".join(risultati)
