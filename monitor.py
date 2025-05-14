import json
import os
from datetime import datetime

LOG_DIR = "log"
os.makedirs(LOG_DIR, exist_ok=True)

def registra_log(dati):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nome_file = f"sessione_{timestamp}.json"
    percorso = os.path.join(LOG_DIR, nome_file)

    dati["timestamp"] = timestamp

    with open(percorso, "w", encoding="utf-8") as f:
        json.dump(dati, f, indent=2, ensure_ascii=False)

    return percorso
