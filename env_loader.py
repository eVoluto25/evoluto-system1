from dotenv import load_dotenv
import os

def carica_variabili_ambiente():
    load_dotenv()
    return {
        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
        "ANTHROPIC_API_KEY": os.getenv("ANTHROPIC_API_KEY"),
        "EMAIL_MITTENTE": os.getenv("EMAIL_MITTENTE"),
        "EMAIL_PASSWORD": os.getenv("EMAIL_PASSWORD"),
        "BASE_URL_OUTPUT": os.getenv("BASE_URL_OUTPUT", "https://tuoprogetto.onrender.com/output/")
    }
