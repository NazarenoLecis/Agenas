# Agenas data analysis

Repository per catalogare, scaricare, normalizzare e analizzare dati pubblici del Servizio sanitario nazionale da fonti istituzionali.

Il progetto integra Agenas, Ministero della Salute, ISTAT, OpenBDAP, AIFA, ISS e fonti regionali ufficiali.

## Obiettivo

Creare una base dati riproducibile per analisi sanitarie nazionali, regionali, aziendali, territoriali, di struttura, di prestazione e di periodo quando la fonte lo consente.

Il repository serve a individuare le fonti disponibili, verificarne licenza e granularita, scaricare i dati quando esistono link diretti, normalizzare i dataset e produrre tabelle, JSON, grafici e notebook di analisi.

## Ambiti coperti

Il progetto mappa dati su mobilita sanitaria, personale, tempi di attesa, costi, spesa, prestazioni, emergenza, ricoveri, attivita ospedaliera, assistenza territoriale, dotazioni, strutture, accreditamento, farmaci, demografia, sorveglianze ISS, fattori di rischio e indicatori di esito.

## Metodologia

Ogni analisi deve riportare fonte, anno, livello territoriale, definizione dell'indicatore e limiti del dato.

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
- usare un solo file requirements.txt;
- creare script per download CSV e JSON;
- creare notebook per analisi e grafici.

## Uso

Installare le dipendenze.

```bash
pip install -r requirements.txt
```

Eseguire la pipeline principale.

```bash
python src/20_run_all.py
```

Script aggiuntivi utili.

```bash
python src/33_validate_discovered_links.py
python src/34_dataset_registry.py
python src/37_source_ranking.py
python src/23_source_audit.py
```

## Output

- data_catalog/data_catalog.csv
- data_catalog/analysis_modules.csv
- data_catalog/discovered_links.csv
- metadata/downloads_log.csv
- data/processed/
- outputs/figures/
- outputs/tables/
- outputs/dashboard_data/
