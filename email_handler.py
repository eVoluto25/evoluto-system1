import smtplib
from email.mime.text import MIMEText
import os

def invia_email(corpo, oggetto, destinatario):
    email_mittente = os.getenv("EMAIL_ADDRESS")
    password = os.getenv("EMAIL_PASSWORD")

    # 🔧 Pulizia del testo per compatibilità utf-8
    if isinstance(corpo, bytes):
        corpo = corpo.decode("utf-8", "ignore")
    corpo = corpo.replace("\xa0", " ").encode("utf-8", "ignore").decode("utf-8")

    msg = MIMEText(corpo, "plain", "utf-8")
    msg["Subject"] = oggetto
    msg["From"] = email_mittente
    msg["To"] = destinatario

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(email_mittente, password)
        server.sendmail(email_mittente, destinatario, msg.as_string())
