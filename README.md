
# eVoluto – Verifica Aziendale Intelligente con AI

**eVoluto** è un sistema completamente automatizzato che:
- riceve bilanci aziendali in PDF,
- li analizza con GPT e Claude,
- incrocia i dati con bandi pubblici compatibili (open data),
- genera una relazione personalizzata per l'impresa.

---

## 🧠 Componenti principali

| Modulo               | Descrizione |
|----------------------|-------------|
| `main.py`            | Endpoint FastAPI attivo su Render |
| `pipeline.py`        | Orchestratore del processo completo |
| `estrazione_pdf.py`  | Estrazione testo dal PDF ricevuto |
| `analisi_blocchi_gpt.py` | Frammenta e analizza via GPT (con delay per evitare limiti) |
| `gpt_module.py`      | Chiamate a GPT-3.5 o GPT-4 |
| `claude_module.py`   | Sintesi dei risultati tecnici |
| `parser_bandi.py`    | Estrae dataset CSV da fonti pubbliche open data |
| `matching_bandi.py`  | Incrocia caratteristiche aziendali con i bandi raccolti |
| `invio_email.py`     | Invio relazione al cliente finale via Gmail |

---

## 🗂️ Aggiornamento automatico bandi

![🔁 Workflow GitHub](https://github.com/matteoparis/evoluto/actions/workflows/update_bandi.yml/badge.svg)
![🕒 Ultimo aggiornamento](https://img.shields.io/github/last-commit/eVoluto25/evoluto-system1/dataset_bandi.csv?label=Ultimo%20aggiornamento%20dataset_bandi.csv)

Il sistema estrae periodicamente nuovi bandi dalle seguenti fonti ufficiali:

- [Incentivi.gov – Portale ufficiale open data](https://www.incentivi.gov.it/it/open-data)
- [PONIC.gov – Open data progetti e incentivi](https://www.ponic.gov.it/open-data/datasets)

Il sistema estrae periodicamente nuovi bandi dalle seguenti fonti ufficiali:

- [Incentivi.gov – Portale ufficiale open data](https://www.incentivi.gov.it/it/open-data)
- [PON Governance – Dataset pubblici](https://www.ponic.gov.it/open-data/datasets)

Ogni 15 giorni, un job automatico GitHub Actions esegue lo script `aggiorna_bandi.py`, che aggiorna `dataset_bandi.csv` in base ai file più recenti disponibili online.

---

## 🚀 Come funziona il flusso

1. L’utente compila un form sul sito WordPress con il bilancio in PDF.
2. Un webhook Make attiva l’endpoint `/analizza-pdf`.
3. Il file viene salvato e letto.
4. GPT esegue l’analisi tecnica per blocchi.
5. Claude sintetizza i risultati in linguaggio strategico.
6. Viene eseguito il matching con i bandi pubblici raccolti.
7. Il tutto viene inviato via email in 3 giorni lavorativi.

---

## 📦 Output generato

- `output/output_gpt.txt` → Analisi tecnica (multi-blocco)
- `output/relazione_finale.txt` → Sintesi Claude + suggerimenti
- `dataset_bandi.csv` → Bandi disponibili, aggiornati via scraping
- `caratteristiche_azienda.csv` → Profilo impresa da confrontare

---

## 📁 Struttura repository

```
.github/workflows/update_bandi.yml
main.py
pipeline.py
aggiorna_bandi.py
parser_bandi.py
matching_bandi.py
estrazione_pdf.py
analisi_blocchi_gpt.py
gpt_module.py
claude_module.py
invio_email.py
input/
  └── documento.pdf
output/
  └── output_gpt.txt
  └── relazione_finale.txt
dataset_bandi.csv
```

---

## 🛠 Requisiti tecnici

- Python 3.10+
- Render (FastAPI hosting)
- Make.com (form e webhook)
- OpenAI API (GPT-3.5 / GPT-4)
- Claude API (Anthropic)
- BeautifulSoup + Requests per scraping
