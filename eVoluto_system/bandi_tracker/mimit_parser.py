import csv
import json

def parse_mimit_csv():
    input_path = "dataset_mimit.csv"
    output_path = "bandi_mimit.json"
    bandi = []

    try:
        with open(input_path, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                codice = row.get("ID_Incentivo")
                titolo = row.get("Titolo")
                descrizione = row.get("Descrizione")
                finalita = row.get("Obiettivo_Finalita")

                if codice and titolo:
                    bandi.append({
                        "fonte": "MIMIT",
                        "codice": codice.strip(),
                        "titolo": titolo.strip(),
                        "descrizione": descrizione.strip() if descrizione else None,
                        "finalita": finalita.strip() if finalita else None
                    })

        with open(output_path, mode="w", encoding="utf-8") as f:
            json.dump(bandi, f, indent=2, ensure_ascii=False)

        print(f"Bandi salvati: {len(bandi)}")

    except Exception as e:
        print("Errore durante il parsing del file CSV:", e)

if __name__ == "__main__":
    parse_mimit_csv()