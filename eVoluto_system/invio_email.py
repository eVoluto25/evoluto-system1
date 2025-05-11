# invio_email.py
import smtplib
from email.message import EmailMessage

def invia_email_gmail(subject, body, allegato_path, destinatario):
    EMAIL_ADDRESS = "info@capitaleaziendale.it"
    EMAIL_PASSWORD = "vvkj cybv njee qjts"  

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = destinatario
    msg.set_content(body)

    # Allega file
    with open(allegato_path, "rb") as f:
        file_data = f.read()
        file_name = f.name.split("/")[-1]
        msg.add_attachment(file_data, maintype="application", subtype="pdf", filename=file_name)

    # Invio
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)
