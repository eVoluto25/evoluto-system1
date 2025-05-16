import os
import boto3
from supabase_uploader import upload_html_to_supabase
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_S3_URL")
SUPABASE_ACCESS_KEY = os.getenv("SUPABASE_S3_ACCESS_KEY")
SUPABASE_SECRET_KEY = os.getenv("SUPABASE_S3_SECRET_KEY")
SUPABASE_BUCKET = os.getenv("SUPABASE_BUCKET_NAME")

def upload_html_to_supabase(contenuto_html: str, nome_file: str) -> str:
    session = boto3.session.Session()
    s3 = session.client(
        service_name='s3',
        endpoint_url=SUPABASE_URL,
        aws_access_key_id=SUPABASE_ACCESS_KEY,
        aws_secret_access_key=SUPABASE_SECRET_KEY,
        region_name='eu-central-1'
    )
    with open(local_file_path, "rb") as f:
        s3.upload_fileobj(f, SUPABASE_BUCKET, supabase_path)
    print(f"✅ File caricato su Supabase: {supabase_path}")
