def analisi_completa_multipla(testo: str) -> str:
    """
    Analizza il testo suddividendolo in blocchi, evitando di superare i limiti dei token
    e assicurando il salvataggio progressivo per poter riprendere in caso di interruzioni.
    """
    import os
    from dividi_blocchi import dividi_blocchi  # Assicurati che esista questa funzione
    from gpt_module import analisi_tecnica_gpt  # Funzione che chiama GPT

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
