# Completamento operativo

Il progetto ora include una pipeline completa per catalogo, discovery, validazione, registry, spesa sanitaria, denominatori demografici, deflatori, output CSV/JSON, controlli qualita e audit statico.

## Pipeline principale

```bash
python src/20_run_all.py
```

## Moduli aggiunti

```text
src/47_openbdap_ckan_health_expenditure.py
src/48_istat_demography_discovery.py
src/49_siope_discovery.py
src/50_health_expenditure_registry.py
src/51_health_expenditure_resource_plan.py
src/52_build_health_expenditure_framework.py
src/54_project_audit.py
```

## Output aggiunti

```text
outputs/tables/openbdap_health_expenditure_resources.csv
outputs/tables/openbdap_health_expenditure_resources.json
outputs/tables/istat_demography_links.csv
outputs/tables/istat_demography_links.json
outputs/tables/siope_links.csv
outputs/tables/siope_links.json
outputs/tables/health_expenditure_registry.csv
outputs/tables/health_expenditure_registry.json
outputs/tables/health_expenditure_resource_plan.csv
outputs/tables/health_expenditure_resource_plan.json
outputs/tables/project_audit.csv
outputs/tables/project_audit.json
outputs/reports/project_audit.md
```

## Logica dati

OpenBDAP / RGS viene interrogato tramite API CKAN per individuare dataset candidati su Conto Economico SSN, spesa sanitaria e movimenti di cassa.

SIOPE viene trattato come fonte di cassa. I relativi dati restano distinti dal Conto Economico attraverso `accounting_basis = cassa_siope`.

ISTAT Demo viene trattato come fonte per popolazione residente, eta, sesso e denominatori demografici.

Il modulo spesa sanitaria produce indicatori nominali, reali, pro capite e per popolazione rilevante.

## Controlli

```bash
python src/54_project_audit.py
```

Il controllo statico verifica sintassi Python, duplicati di identificativi, schema delle fonti, coerenza tra tema e moduli, configurazione del modulo spesa sanitaria e coppie CSV/JSON.
