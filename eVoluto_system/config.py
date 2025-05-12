import os
from dotenv import load_dotenv

# Carica le variabili d'ambiente dal file .env (se presente)
load_dotenv()

# === CONFIGURAZIONI DI BASE ===
OUTPUT_DIR = "output"
ALLEGATI_DIR = "allegati"
BANDI_PATH = "bando_tracker/dataset_bandi.csv"

# === CONFIGURAZIONE EMAIL ===
EMAIL_MITTENTE = os.getenv("EMAIL_MITTENTE", "verifica.evoluto@gmail.com")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")  # App password per Gmail
EMAIL_DESTINATARIO = os.getenv("EMAIL_DESTINATARIO", "info@capitaleaziendale.it")

# === CONFIGURAZIONE AI ===
API_KEY_GPT = os.getenv("API_KEY_GPT")
API_KEY_CLAUDE = os.getenv("API_KEY_CLAUDE")

# === IMPOSTAZIONI DI SERVIZIO ===
DEFAULT_PERIODO_ANALISI = "Ultimo bilancio disponibile"
MAX_FILE_SIZE_MB = 10
