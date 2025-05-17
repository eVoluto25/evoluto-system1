from aggiorna_bandi import file_aggiornato, scarica_file, DATASET_URL, ETAG_FILE, DATASET_FILE

def aggiorna_bandi():
    if file_aggiornato(DATASET_URL, ETAG_FILE):
        scarica_file(DATASET_URL, DATASET_FILE)
    else:
        print("⏭️ Nessun aggiornamento disponibile. Dataset invariato.")
