import imaplib
import email
from email.header import decode_header
import os

def recupera_email_con_allegati():
    email_address = "verifica.evoluto@gmail.com"
    password = "vvkj cybv njee qjts"

    try:
        print("► Connessione al server IMAP in corso...")
        imap = imaplib.IMAP4_SSL("imap.gmail.com")
        imap.login(email_address, password)
        imap.select("INBOX")

        # Cerca le email non lette
        status, messages = imap.search(None, 'UNSEEN')
        if status != "OK":
            print("✘ Errore nella ricerca delle email.")
            return None

        msg_ids = messages[0].split()
        print(f"► Email non lette trovate: {len(msg_ids)}")

        allegati = []

        for num in msg_ids:
            status, msg_data = imap.fetch(num, "(RFC822)")
            if status != "OK":
                print(f"✘ Errore nel recupero del messaggio {num.decode()}")
                continue

            msg = email.message_from_bytes(msg_data[0][1])
            subject, encoding = decode_header(msg["Subject"])[0]
            subject = subject.decode(encoding) if isinstance(subject, bytes) else subject
            print(f"\n📧 Email: {subject}")

            for part in msg.walk():
                if part.get_content_maintype() == 'multipart':
                    continue
                if part.get('Content-Disposition') is None:
                    continue

                filename = part.get_filename()
                if filename and filename.lower().endswith(".pdf"):
                    print(f"📎 Allegato PDF trovato: {filename}")
                    filepath = os.path.join("estratti_pdf", filename)
                    with open(filepath, "wb") as f:
                        f.write(part.get_payload(decode=True))
                    allegati.append(filepath)

        imap.logout()

        if allegati:
            print(f"✅ Totale allegati PDF ricevuti: {len(allegati)}")
            for nome in allegati:
                print(f"– {os.path.basename(nome)}")
            return allegati[0]  # Usa solo il primo per il processo
        else:
            print("⚠️ Nessun allegato PDF trovato.")
            return None

    except Exception as e:
        print("Errore:", e)
        return None