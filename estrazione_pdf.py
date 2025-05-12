def estrai_testo_da_pdf(file_path):
    with open(file_path, "rb") as f:
        return f.read().decode("utf-8", errors="ignore")
