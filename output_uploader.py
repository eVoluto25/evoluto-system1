import os
from uuid import uuid4

OUTPUT_DIR = "output"
BASE_URL = "https://evoluto-system1.onrender.com"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def salva_output_html(titolo, contenuto):
    file_id = uuid4().hex
    nome_file = f"{titolo}_{file_id}.html".replace(" ", "_")
    percorso_file = os.path.join(OUTPUT_DIR, nome_file)

    html = f"""<!DOCTYPE html>
<html lang='it'>
<head>
    <meta charset='UTF-8'>
    <title>{titolo}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #f9f9f9;
            padding: 40px;
            max-width: 800px;
            margin: auto;
        }}
        h1 {{
            color: #333;
        }}
        pre {{
            background-color: #eee;
            padding: 20px;
            border-radius: 5px;
            white-space: pre-wrap;
            word-wrap: break-word;
        }}
    </style>
</head>
<body>
    <h1>{titolo}</h1>
    <pre>{contenuto}</pre>
</body>
</html>
"""

    with open(percorso_file, "w", encoding="utf-8") as f:
        f.write(html)

    return BASE_URL + nome_file
