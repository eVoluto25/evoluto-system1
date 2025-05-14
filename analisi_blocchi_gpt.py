import os
import logging
import requests
from gpt_module import analisi_completa_multipla
from email_handler import invia_email

# ✅ Funzione per dividere il testo in blocchi
def dividi_blocchi(testo: str, max_caratteri: int = 10000) -> list:
    return [testo[i:i + max_caratteri] for i in range(0, len(testo), max_caratteri)]

# ✅ Funzione principale
def analisi_completa_multipla(testo):
    # 🧼 Pulizia del testo da caratteri non compatibili con UTF-8
    testo = testo.encode("utf-8", "ignore").decode("utf-8")
    
    blocchi = dividi_blocchi(testo)
    risultati = []
for i, blocco in enumerate(blocchi):
    path_blocco = f"blocco_{i+1}.txt"

    # 📂 Check se esiste il file già salvato
    if os.path.exists(path_blocco):
        try:
            with open(path_blocco, "r") as f:
                risultati.append(f.read())
                continue
         except Exception as e:
             logging.warning(f"⚠️ Errore lettura blocco salvato {i+1}: {e}")

        # 🤖 Analisi GPT del blocco
        try:
            logging.info(f"📤 GPT – Invio blocco {i+1} di {len(blocchi)}")
             risposta = analisi_tecnica_gpt(blocco)
            
        if not risposta or len(risposta.strip()) < 10:
            raise ValueError("Risposta GPT troppo corta o vuota")
        risultati.append(risposta)

        # 💾 Salvataggio file
        with open(path_blocco, "w") as f:
            f.write(risposta)
  
    except Exception as e:
        logging.error(f"❌ Errore nel blocco {i+1}: {e}")
        risultati.append(f"[ERRORE BLOCCO {i+1}] GPT non ha fornito una risposta valida.")
        continue

        if os.path.exists(path_blocco):
            with open(path_blocco, "r") as f:
                risultati.append(f.read())
            continue

        try:
            risposta = analisi_completa_multipla(blocco, "", "")
            risultati.append(risposta)

            with open(path_blocco, "w") as f:
                f.write(risposta)

        except Exception as e:
            print(f"Errore nel blocco {i+1}:", e)
            parziale = "\n\n".join(risultati)
            corpo_email = f"⚠️ GPT si è interrotto al blocco {i+1}.\n\nEcco l'analisi parziale prodotta finora:\n\n{parziale[:10000]}"

            # Invia email parziale
            invia_email(
                destinatario="info@capitaleaziendale.it",
                oggetto=f"⚠️ Analisi GPT interrotta al blocco {i+1}",
                corpo=corpo_email
            )
            return parziale

    output_gpt = "\n\n".join(risultati)

    # ✅ Salva output completo in file pubblico
    with open("uploads/output_gpt.txt", "w") as f:
        f.write(output_gpt)

    # ✅ Invia email tramite Make
    requests.post(
        "https://hook.eu2.make.com/WEBHOOK_GPT",  # 🔁 Sostituisci con il tuo webhook reale
        json={
            "subject": "🧠 Analisi GPT completata",
            "body": "Analisi GPT completata con successo.\n\n📎 Scarica l'analisi tecnica completa:\nhttps://TUA-APP-RENDER.onrender.com/uploads/output_gpt.txt"
        }
    )

    return output_gpt
