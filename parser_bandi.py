CONFIG_FILE = "config_siti_bandi.json"
OUTPUT_FILE = "dataset_bandi.csv"


def carica_url_da_config():
    import json
    with open(CONFIG_FILE, "r") as f:
        data = json.load(f)
    return data["urls"]


def estrai_link_csv_da_html(base_url):
    try:
        response = requests.get(base_url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        link_file = []

        for a_tag in soup.find_all("a", href=True):
            href = a_tag["href"]
            if any(ext in href.lower() for ext in [".csv", ".xls", ".xlsx"]):
                full_url = urljoin(base_url, href)
                link_file.append(full_url)

        return link_file

    except Exception as e:
        print(f"Errore su {base_url}: {e}")
        return []


def scarica_e_aggiungi_dati_csv(url, writer):
    try:
        response = requests.get(url, timeout=15)
        response.encoding = 'utf-8'

        lines = response.text.splitlines()
        csv_reader = csv.reader(lines)

        for row in csv_reader:
            writer.writerow(row)

        print(f"✔️ Scaricato: {url}")
    except Exception as e:
        print(f"❌ Errore su {url}: {e}")


def aggiorna_dataset():
    urls = carica_url_da_config()
    all_links = []

    for sito in urls:
        print(f"🔎 Analizzo {sito}")
        links = estrai_link_csv_da_html(sito)
        all_links.extend(links)

    with open(OUTPUT_FILE, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for link in all_links:
            scarica_e_aggiungi_dati_csv(link, writer)


if __name__ == "__main__":
    aggiorna_dataset()
