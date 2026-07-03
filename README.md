# Agenas data analysis

Repository per catalogare, scaricare, normalizzare e analizzare dati pubblici del Servizio sanitario nazionale da fonti istituzionali.

Il progetto parte da Agenas e integra Ministero della Salute, ISTAT e fonti regionali ufficiali.

## Obiettivo

Costruire una base dati riproducibile per analisi nazionali, regionali e territoriali su capacita ospedaliera, strutture, posti letto, grandi apparecchiature, mobilita sanitaria, liste di attesa, indicatori PNE, assistenza territoriale e accessibilita ai servizi.

## Moduli prioritari

La parte centrale del progetto e la mobilita sanitaria. Serve capire da dove partono i pazienti, dove vanno, per quali prestazioni, con quale valore economico e con quale livello di complessita. La mobilita va distinta tra prestazioni di prossimita, bassa complessita e alta specializzazione.

Gli altri moduli prioritari sono personale sanitario, tempi di attesa, costi, prestazioni, emergenza, ricoveri e attivita ospedaliera.

Per il personale servono distribuzioni di medici per categoria o disciplina, infermieri, operatori socio sanitari e altre professioni. Per le prestazioni servono numero, tipo, territorio, struttura e periodo. Per emergenza servono accessi, triage, tempi, esiti e ricoveri successivi.

## Metodologia

Ogni analisi deve riportare fonte, anno, livello territoriale, definizione dell'indicatore e limiti del dato.

I livelli territoriali principali sono nazionale, regionale, aziendale, struttura e prestazione.

Gli indicatori non devono essere letti come giudizi automatici. Le differenze tra territori e strutture possono dipendere da codifiche, volumi, composizione dei casi, disponibilita dei dati e criteri di inclusione.

Il PNE deve essere usato come fonte di indicatori comparativi. Il repository non deve trasformarlo in una classifica secca di strutture.

## Regole del codice

- usare file utils per le funzioni riutilizzabili;
- non usare classi;
- non usare argparse;
- non creare file __init__.py;
- scrivere commenti estensivi;
- usare config/project_config.py per la configurazione;
- non usare file YAML per la configurazione;
- creare script per download CSV e JSON;
- creare notebook per analisi e grafici.

## Uso

Installare le dipendenze.

```bash
pip install -r requirements.txt
```

Eseguire gli script in ordine.

```bash
python src/00_discover_sources.py
python src/01_download_ministero_salute.py
python src/02_download_Agenas.py
python src/03_normalize_ministero_salute.py
python src/04_normalize_Agenas.py
python src/05_build_indicators.py
python src/06_export_json.py
python src/07_build_charts.py
```

Aprire poi i notebook nella cartella notebooks.

## Output

- data_catalog/data_catalog.csv
- metadata/downloads_log.csv
- data/processed/
- outputs/figures/
- outputs/tables/
- outputs/dashboard_data/
