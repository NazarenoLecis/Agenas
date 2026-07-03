# Agenas data analysis

Repository per catalogare, scaricare, normalizzare e analizzare dati pubblici del Servizio sanitario nazionale da fonti istituzionali.

Il progetto integra Agenas, Ministero della Salute, ISTAT, OpenBDAP, AIFA, ISS e fonti regionali ufficiali.

## Cosa fa il progetto

Il progetto cerca fonti sanitarie pubbliche, identifica link a dataset e report, verifica quali contenuti sono scaricabili, costruisce un catalogo delle fonti e prepara dati normalizzati per analisi nazionali, regionali, aziendali, territoriali, di struttura, di prestazione e di periodo quando la fonte lo consente.

Il repository produce tabelle, file JSON, grafici, inventari, report di qualita e notebook di analisi. I dati grezzi e gli output pesanti vengono generati localmente e non sono salvati nel repository.

## Ambiti coperti

Il progetto mappa dati su mobilita sanitaria, personale, tempi di attesa, costi, spesa, prestazioni, emergenza, ricoveri, attivita ospedaliera, assistenza territoriale, dotazioni, strutture, accreditamento, farmaci, demografia, sorveglianze ISS, fattori di rischio e indicatori di esito.

## Fonti

Le fonti principali sono:

- Agenas
- Ministero della Salute
- ISTAT
- OpenBDAP / Ragioneria Generale dello Stato
- AIFA
- ISS
- portali open data regionali

Ogni fonte viene classificata in base a disponibilita del dato, formato, licenza, granularita, metodo di accesso e possibilita di riuso.

## Come usare il repository

Installare le dipendenze.

```bash
pip install -r requirements.txt
```

Eseguire la pipeline principale.

```bash
python src/20_run_all.py
```

La pipeline crea o aggiorna cataloghi, discovery dei link, validazione dei link, registro dataset, normalizzazione, tabelle di output, grafici e database locale DuckDB.

## Output principali

Dopo l'esecuzione della pipeline, controllare soprattutto:

```text
data_catalog/data_catalog.csv
data_catalog/analysis_modules.csv
data_catalog/discovered_links.csv
outputs/tables/recursive_public_discovery.csv
outputs/tables/agenas_links.csv
outputs/tables/ministero_all_links.csv
outputs/tables/iss_links.csv
outputs/tables/validated_discovered_links.csv
outputs/tables/dataset_registry.csv
outputs/tables/source_ranking.csv
outputs/tables/quality_overview.csv
outputs/reports/source_audit.md
```

I dataset processati vengono salvati in:

```text
data/processed/
```

Gli output per dashboard vengono salvati in:

```text
outputs/dashboard_data/
```

## Come leggere gli output

`data_catalog/data_catalog.csv` contiene le fonti configurate.

`data_catalog/discovered_links.csv` contiene i link trovati nelle pagine pubbliche.

`outputs/tables/validated_discovered_links.csv` contiene i link testati con informazioni su status code, content type e URL finale.

`outputs/tables/dataset_registry.csv` combina fonti configurate e link trovati, e serve come base per decidere quali dataset scaricare davvero.

`outputs/tables/source_ranking.csv` ordina le fonti in base a priorita operativa.

`outputs/tables/quality_overview.csv` contiene controlli minimi sui dataset processati.

## Limiti

Il repository usa solo fonti pubbliche. Non accede ad aree riservate, non usa credenziali e non tenta di scaricare dati personali o microdati sanitari non pubblici.

Non tutte le fonti pubbliche espongono dataset scaricabili. Alcune fonti sono dashboard, report PDF o pagine informative. In questi casi il repository salva metadati e link utili, lasciando la fonte in revisione manuale.

Gli indicatori sanitari dipendono da definizioni, codifiche, volumi, composizione dei casi, copertura del dato e criteri di inclusione. Ogni analisi deve essere letta insieme alla fonte e alle note metodologiche.

## Struttura principale

```text
config/project_config.py      configurazione delle fonti e dei moduli
src/                          script di discovery, download, normalizzazione e analisi
data_catalog/                 cataloghi generati dalla pipeline
data/                         dati grezzi e processati generati localmente
outputs/                      tabelle, grafici, report e JSON per dashboard
notebooks/                    notebook di esplorazione e analisi
```
