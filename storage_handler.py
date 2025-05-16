import os
import requests
from datetime import datetime

def upload_html_to_supabase(contenuto_html: str, nome_file: str) -> str:
    """
    Carica un contenuto HTML su Supabase e restituisce il link pubblico.

    :param contenuto_html: Contenuto HTML da caricare
    :param nome_file: Nome del file HTML (senza estensione)
    :return: URL pubblico del file caricato
    """

    supabase_url = os.getenv("SUPABASE_S3_URL")
    supabase_bucket = os.getenv("SUPABASE_BUCKET_NAME")
    supabase_access_key = os.getenv("SUPABASE_S3_ACCESS_KEY")

    if not all([supabase_url, supabase_bucket, supabase_access_key]):
        raise EnvironmentError("Variabili d'ambiente Supabase mancanti")

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    path_remoto = f"{nome_file}_{timestamp}.html"
    url_upload = f"{supabase_url}/storage/v1/object/{supabase_bucket}/{path_remoto}"

    headers = {
       "Authorization": supabase_access_key,  # ✅ solo la chiave, niente "Bearer"
    "Content-Type": "text/html; charset=utf-8"
    }

    response = requests.put(url_upload, data=contenuto_html.encode("utf-8"), headers=headers)

    if response.status_code >= 400:
        raise RuntimeError(f"Errore upload HTML: {response.status_code} - {response.text}")

    return url_upload
