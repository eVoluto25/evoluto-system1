import requests
import logging

def invia_a_make(payload: dict):
    try:
        response = requests.post("https://hook.eu2.make.com/de2f0hpi3elrsfewa2tfptcmjfib94uw", json=payload)
        response.raise_for_status()
        print("✅ Dati inviati correttamente a Make.")
    except requests.exceptions.RequestException as e:
        print(f"❌ Errore invio Make: {e}")
        logging.warning(f"❌ Errore durante l'invio a Make: {e}")
