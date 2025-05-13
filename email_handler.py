import smtplib
from email.mime.text import MIMEText
import logging
import os

def invia_email(destinatario, oggetto, corpo):
    try:
        email_mittente = os.getenv("EMAIL_MITTENTE")
        password = os.getenv("EMAIL_PASSWORD")

        msg = MIMEText(corpo, "plain", "utf-8")
        msg["Subject"] = oggetto
        msg["From"] = email_mittente
        msg["To"] = destinatario

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(email_mittente, password)
            server.send_message(msg)

        logging.info("✅ Email inviata correttamente")

    except Exception as e:
        logging.error(f"❌ Errore durante l'invio email: {e}")
