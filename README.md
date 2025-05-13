# eVoluto System

Questo progetto è un sistema di analisi aziendale che utilizza AI per fare analisi predittive e supportare le decisioni aziendali, in particolare nell'ambito delle analisi finanziarie e del matching con bandi di finanza agevolata.



## 🔄 Aggiornamento automatico bandi

![Aggiornamento bandi](https://github.com/matteoparis/evoluto/actions/workflows/update_bandi.yml/badge.svg)

L’elenco dei bandi pubblici viene aggiornato automaticamente ogni 15 giorni tramite GitHub Actions.

Le fonti ufficiali tracciate includono:
- [Incentivi.gov – Portale ufficiale incentivi nazionali](https://www.incentivi.gov.it/it/open-data)
- [PON Governance – Dataset Open Data](https://www.ponic.gov.it/open-data/datasets)

I dati aggiornati vengono salvati in `dataset_bandi.csv` e usati per il matching con i bilanci aziendali tramite `matching_bandi.py`.




![Aggiornamento bandi](https://github.com/matteoparis/evoluto/actions/workflows/update_bandi.yml/badge.svg)

L’elenco dei bandi pubblici viene aggiornato automaticamente ogni 15 giorni tramite GitHub Actions.

Le fonti attualmente tracciate includono:
- Lazio Innova
- Regione Lazio (Open Data)
- Camere di Commercio del Lazio

I dati aggiornati vengono salvati in `dataset_bandi.csv` e usati per il matching con i bilanci aziendali tramite `matching_bandi.py`.
## Setup
Per eseguire il progetto, assicurati di avere Python 3.x installato e esegui:
## Funzionalità
- Estrazione dati da PDF
- Analisi del bilancio aziendale
- Matching con bandi

## Come Usare
Dopo aver configurato le dipendenze, avvia il server:uvicorn main:app –host 0.0.0.0 –port 10000
