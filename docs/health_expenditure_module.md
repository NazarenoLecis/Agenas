# Modulo spesa sanitaria regionale

File principali:

```text
config/health_expenditure_config.py
src/52_build_health_expenditure_framework.py
src/54_project_audit.py
metadata/health_expenditure_note.md
```

Il modulo e agganciato alla pipeline principale:

```bash
python src/20_run_all.py
```

Puo essere eseguito anche da solo:

```bash
python src/52_build_health_expenditure_framework.py
```

Il modulo produce sempre CSV e JSON.

Output principali:

```text
outputs/tables/health_expenditure_source_plan.csv
outputs/tables/health_expenditure_required_schema.csv
outputs/tables/health_expenditure_denominator_dictionary.csv
outputs/tables/health_expenditure_denominator_rules.csv
outputs/tables/regional_health_expenditure_demographic_adjusted.csv

data/processed/demography/demographic_denominators_region_year.csv
data/processed/prices/price_deflators.csv
data/processed/health_expenditure/regional_health_expenditure_nominal_real.csv
data/processed/health_expenditure/regional_health_expenditure_demographic_adjusted.csv
```

I file JSON equivalenti vengono generati negli stessi folder.

Fonti previste:

- OpenBDAP / RGS per Conto Economico degli enti del SSN
- SIOPE / RGS per pagamenti e incassi di cassa
- ISTAT per popolazione, nascite e deflatori

Schema finale:

```text
year
region_code
region_name
source
accounting_basis
spending_area
spending_item_code
spending_item_name
amount_nominal_eur
amount_real_eur
price_base_year
deflator_used
population_total
population_0
population_0_4
population_0_14
population_0_17
births
women_15_49
population_65_plus
population_75_plus
population_80_plus
amount_per_capita
amount_real_per_capita
amount_per_relevant_population
amount_real_per_relevant_population
relevant_population_type
relevant_population_value
```

Il modulo evita il doppio conteggio dei denominatori quando la fonte contiene insieme righe Totale, Maschi e Femmine. Se esistono righe Totale per eta, usa quelle per la popolazione totale e per le fasce 0-4, 0-14, 65+, 75+ e 80+. Per `women_15_49` usa solo righe femminili.

Regole di denominatore:

```text
nascite, parti, neonatologia                  births
infanzia                                      population_0_4
pediatria, minori                             population_0_14
consultori, gravidanza, salute riproduttiva   women_15_49
RSA, ADI anziani, non autosufficienza         population_80_plus
lungodegenza, fragilita                       population_75_plus
anziani, cronicita, geriatria                 population_65_plus
altre voci                                    population_total
```

Nota metodologica:

Il Conto Economico misura costi e ricavi di competenza.

SIOPE misura incassi e pagamenti di cassa.

La spesa pro capite generale e utile per una prima lettura. Per molte voci sanitarie il denominatore piu informativo e una popolazione specifica. Le spese legate a natalita e neonatologia vanno rapportate a nascite o popolazione infantile. Le spese legate a cronicita, RSA, ADI, fragilita e lungodegenza vanno lette anche rispetto alla popolazione anziana.
