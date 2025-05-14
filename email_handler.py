import smtplib
from email.mime.text import MIMEText
import os

def invia_email(corpo, oggetto, destinatario):
    email_mittente = os.getenv("EMAIL_ADDRESS")
    password = os.getenv("EMAIL_PASSWORD")

    # Pulizia del testo da caratteri invisibili e compatibilità
    if isinstance(corpo, bytes):
        corpo = corpo.decode("utf-8", "ignore")

    corpo = (
        corpo.replace("\xa0", " ")
             .replace("\u202f", " ")
             .replace("\ufeff", "")
             .strip()
    )

    # Fallback se stringa vuota
    if not corpo.strip():
        corpo = "⚠️ Attenzione: il testo della relazione è vuoto o non leggibile."

    # Costruzione email
    msg = MIMEText(corpo, "plain", "utf-8")
    msg["Subject"] = oggetto
    msg["From"] = email_mittente
    msg["To"] = destinatario

    # Invio
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(email_mittente, password)
        server.sendmail(email_mittente, destinatario, msg.as_string())
