import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
import os

def invia_email_gmail(file_path):
    mittente = "verifica.evoluto@gmail.com"
    destinatario = "info@capitaleaziendale.it"
    password = os.getenv("GMAIL_APP_PASSWORD")  # ⚠️ La password va definita come variabile d’ambiente su Render

    oggetto = "📊 Analisi aziendale completata – eVoluto"
    corpo_email = (
        "Ciao,\n\nin allegato trovi la relazione tecnica finale generata dal sistema eVoluto.\n\n"
        "Se hai bisogno di ulteriori approfondimenti o vuoi attivare un confronto operativo, siamo a disposizione.\n\n"
        "Cordiali saluti,\n\nIl Team Capitale Aziendale"
    )

    # Costruzione messaggio
    msg = MIMEMultipart()
    msg["From"] = mittente
    msg["To"] = destinatario
    msg["Subject"] = oggetto
    msg.attach(MIMEText(corpo_email, "plain"))

    # Allegato
    with open(file_path, "rb") as f:
        part = MIMEApplication(f.read(), Name=os.path.basename(file_path))
        part["Content-Disposition"] = f'attachment; filename="{os.path.basename(file_path)}"'
        msg.attach(part)

    # Invio email
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(mittente, password)
        server.send_message(msg)
