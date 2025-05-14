import smtplib
from email.message import EmailMessage
from env_loader import carica_variabili_ambiente
import logging

def invia_email(destinatario, oggetto, corpo):
    config = carica_variabili_ambiente()
    mittente = config["EMAIL_MITTENTE"]
    password = config["EMAIL_PASSWORD"]

    msg = EmailMessage()
    msg["Subject"] = oggetto
    msg["From"] = mittente
    msg["To"] = destinatario
    msg.set_content(corpo)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(mittente, password)
            server.send_message(msg)
            logging.info("Email inviata con successo")
    except Exception as e:
        logging.error(f"Errore invio email: {e}")
