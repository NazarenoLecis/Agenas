# AGENAS data analysis

Repository per catalogare, scaricare, normalizzare e analizzare dati pubblici del Servizio sanitario nazionale da fonti istituzionali.

## Obiettivo

Costruire una base dati riproducibile per analisi nazionali, regionali e territoriali.

## Regole del codice

- usare file utils per le funzioni riutilizzabili;
- non usare classi;
- non usare argparse;
- non creare file __init__.py;
- scrivere commenti estensivi;
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
python src/02_download_agenas.py
python src/03_normalize_ministero_salute.py
python src/04_normalize_agenas.py
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
