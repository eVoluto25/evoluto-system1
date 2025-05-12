import os
from pathlib import Path
from dotenv import load_dotenv

# Carica variabili da .env (opzionale ma utile in ambienti locali o separati)
load_dotenv()

# === 📍 API KEYS ===
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY") or "INSERISCI_LA_TUA_API_KEY_CLAUDE"

# === 📍 EMAIL CONFIG ===
EMAIL_MITTENTE = "verifica.evoluto@gmail.com"
EMAIL_DESTINATARIO = "info@capitaleaziendale.it"
APP_PASSWORD_EMAIL = os.getenv("APP_PASSWORD_EMAIL") or "vvkj cybv njee qjts"  # Password per app Gmail

# === 📍 OUTPUT E FILE SYSTEM ===
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

PDF_SALVATO_PATH = OUTPUT_DIR / "documento.pdf"
RELAZIONE_FINALE_PATH = OUTPUT_DIR / "relazione_finale.txt"
ANALISI_GPT_PATH = OUTPUT_DIR / "output_gpt.txt"

# === 📍 BANDI ===
BANDI_CSV_PATH = Path("bandi_tracker") / "bandi.csv"  # Percorso predefinito ai bandi

# === 📍 PARAMETRI DI SISTEMA ===
DEFAULT_PERIODO = "ultimo bilancio disponibile"
