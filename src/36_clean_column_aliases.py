"""
Script: 36_clean_column_aliases.py

Crea un dizionario base di alias per colonne sanitarie comuni.
"""

import pandas as pd

from utils_paths import get_configured_path, ensure_project_folders
from utils_io import write_csv_json_pair


ALIASES = [
    {"standard_name": "region", "aliases": "regione;regione_nome;region_name;territorio"},
    {"standard_name": "region_code", "aliases": "codice_regione;cod_reg;region_code;codice_territorio"},
    {"standard_name": "year", "aliases": "anno;year;periodo;time"},
    {"standard_name": "origin", "aliases": "origine;regione_origine;regione_residenza"},
    {"standard_name": "destination", "aliases": "destinazione;regione_destinazione;regione_erogazione"},
    {"standard_name": "structure", "aliases": "struttura;ospedale;presidio;istituto"},
    {"standard_name": "service", "aliases": "prestazione;servizio;specialistica"},
    {"standard_name": "volume", "aliases": "volume;volumi;numero;conteggio;n"},
    {"standard_name": "amount_nominal_eur", "aliases": "costo;spesa;importo;valore;amount;amount_nominal_eur"},
    {"standard_name": "accounting_basis", "aliases": "basis;criterio_contabile;competenza_cassa;accounting_basis"},
    {"standard_name": "spending_area", "aliases": "area_spesa;macrovoce;categoria;spending_area"},
    {"standard_name": "spending_item_name", "aliases": "voce;descrizione;descrizione_voce;spending_item_name"},
    {"standard_name": "population_total", "aliases": "popolazione;residenti;population;population_total"},
]


def main():
    ensure_project_folders()
    output_path = get_configured_path("outputs_tables") / "column_aliases.csv"
    write_csv_json_pair(pd.DataFrame(ALIASES), output_path.parent, output_path.stem)
    print(f"Column aliases written to {output_path}")


if __name__ == "__main__":
    main()
