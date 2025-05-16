from supabase_client import supabase
from datetime import datetime

def upload_html_to_supabase(contenuto_html: str, nome_file: str) -> str:
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    remote_path = f"{nome_file}_{timestamp}.html"
    data = contenuto_html.encode("utf-8")

    res = supabase.storage.from_("verifica-aziendale-evoluto").upload(
        remote_path, data, {"content-type": "text/html"}
    )

    if not res:
        raise RuntimeError("Errore durante l'upload su Supabase")

    public_url = supabase.storage.from_("verifica-aziendale-evoluto").get_public_url(remote_path)
    return public_url
