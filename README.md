# Agenas data analysis

Repository per catalogare, scaricare, normalizzare e analizzare dati pubblici del Servizio sanitario nazionale da fonti istituzionali.

Il progetto integra Agenas, Ministero della Salute, ISTAT, OpenBDAP, SIOPE, AIFA, ISS e fonti regionali ufficiali.

## Cosa fa il progetto

Il progetto cerca fonti sanitarie pubbliche, identifica link a dataset e report, verifica quali contenuti sono scaricabili, costruisce un catalogo delle fonti e prepara dati normalizzati per analisi nazionali, regionali, aziendali, territoriali, di struttura, di prestazione e di periodo quando la fonte lo consente.

Il repository produce tabelle, file JSON, grafici, inventari, report di qualita e notebook di analisi. I dati grezzi e gli output pesanti vengono generati localmente e non sono salvati nel repository.

Gli output tabellari pubblici devono essere disponibili sempre in CSV e JSON. Parquet puo essere usato solo come cache tecnica locale.

## Ambiti coperti

Il progetto mappa dati su mobilita sanitaria, personale, tempi di attesa, costi, spesa sanitaria, prestazioni, emergenza, ricoveri, attivita ospedaliera, assistenza territoriale, dotazioni, strutture, accreditamento, farmaci, demografia, sorveglianze ISS, fattori di rischio e indicatori di esito.

Il modulo `health_expenditure` integra spesa nominale, spesa reale, popolazione totale, popolazione per eta, nascite, donne 15-49, popolazione over 65, over 75 e over 80. Gli indicatori finali includono spesa pro capite e spesa per popolazione demografica rilevante.

## Fonti

Le fonti principali sono:

- Agenas
- Ministero della Salute
- ISTAT
- OpenBDAP / Ragioneria Generale dello Stato
- SIOPE
- AIFA
- ISS
- portali open data regionali

Ogni fonte viene classificata in base a disponibilita del dato, formato, licenza, granularita, metodo di accesso e possibilita di riuso.

Per la spesa sanitaria annuale regionale la fonte principale prevista e il Conto Economico degli enti del SSN da OpenBDAP / RGS. SIOPE viene trattato come fonte di cassa per incassi e pagamenti, tenuto separato tramite il campo `accounting_basis`.

## Come usare il repository

Installare le dipendenze.

```bash
pip install -r requirements.txt
```

Eseguire la pipeline principale.

```bash
python src/20_run_all.py
```

Eseguire solo il modulo spesa sanitaria.

```bash
python src/52_build_health_expenditure_framework.py
```

Eseguire il controllo statico del progetto.

```bash
python src/54_project_audit.py
```

La pipeline crea o aggiorna cataloghi, discovery dei link, validazione dei link, registro dataset, normalizzazione, tabelle di output, grafici, controlli di qualita, audit statico e database locale DuckDB.

## Output principali

Dopo l'esecuzione della pipeline, controllare soprattutto:

```text
data_catalog/data_catalog.csv
data_catalog/data_catalog.json
data_catalog/analysis_modules.csv
data_catalog/analysis_modules.json
data_catalog/discovered_links.csv
data_catalog/discovered_links.json
outputs/tables/recursive_public_discovery.csv
outputs/tables/recursive_public_discovery.json
outputs/tables/validated_discovered_links.csv
outputs/tables/validated_discovered_links.json
outputs/tables/dataset_registry.csv
outputs/tables/dataset_registry.json
outputs/tables/source_ranking.csv
outputs/tables/source_ranking.json
outputs/tables/quality_overview.csv
outputs/tables/quality_overview.json
outputs/tables/project_audit.csv
outputs/tables/project_audit.json
outputs/reports/source_audit.md
outputs/reports/project_audit.md
```

Output specifici per spesa sanitaria e denominatori:

```text
data/processed/demography/demographic_denominators_region_year.csv
data/processed/demography/demographic_denominators_region_year.json
data/processed/prices/price_deflators.csv
data/processed/prices/price_deflators.json
data/processed/health_expenditure/regional_health_expenditure_nominal_real.csv
data/processed/health_expenditure/regional_health_expenditure_nominal_real.json
data/processed/health_expenditure/regional_health_expenditure_demographic_adjusted.csv
data/processed/health_expenditure/regional_health_expenditure_demographic_adjusted.json
outputs/tables/regional_health_expenditure_demographic_adjusted.csv
outputs/tables/regional_health_expenditure_demographic_adjusted.json
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

`data_catalog/data_catalog.csv` e `data_catalog/data_catalog.json` contengono le fonti configurate.

`data_catalog/discovered_links.csv` e `data_catalog/discovered_links.json` contengono i link trovati nelle pagine pubbliche.

`outputs/tables/validated_discovered_links.csv` contiene i link testati con informazioni su status code, content type e URL finale.

`outputs/tables/dataset_registry.csv` combina fonti configurate e link trovati, e serve come base per decidere quali dataset scaricare davvero.

`outputs/tables/source_ranking.csv` ordina le fonti in base a priorita operativa.

`outputs/tables/quality_overview.csv` contiene controlli minimi sui dataset processati.

`outputs/tables/project_audit.csv` contiene controlli statici su sintassi Python, configurazione, duplicati, temi e coppie CSV/JSON.

## Limiti

Il repository usa solo fonti pubbliche. Non accede ad aree riservate, non usa credenziali e non tenta di scaricare dati personali o microdati sanitari non pubblici.

Non tutte le fonti pubbliche espongono dataset scaricabili. Alcune fonti sono dashboard, report PDF o pagine informative. In questi casi il repository salva metadati e link utili, lasciando la fonte in revisione manuale.

Gli indicatori sanitari dipendono da definizioni, codifiche, volumi, composizione dei casi, copertura del dato e criteri di inclusione. Ogni analisi deve essere letta insieme alla fonte e alle note metodologiche.

La spesa da Conto Economico misura costi e ricavi di competenza. SIOPE misura incassi e pagamenti di cassa. Le due basi non devono essere sommate senza distinguere il campo `accounting_basis`.

## Struttura principale

```text
config/project_config.py                 configurazione delle fonti e dei moduli
config/health_expenditure_config.py      configurazione spesa sanitaria, deflatori e denominatori
src/                                     script di discovery, download, normalizzazione e analisi
data_catalog/                            cataloghi generati dalla pipeline
data/                                    dati grezzi e processati generati localmente
outputs/                                 tabelle, grafici, report e JSON per dashboard
notebooks/                               notebook di esplorazione e analisi
```
