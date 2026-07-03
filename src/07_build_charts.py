"""
Script: 07_build_charts.py

Obiettivo
Creare grafici iniziali dai file tabellari generati dalla pipeline.

Questa prima versione crea un grafico sulla dimensione dei dataset processati.
I grafici sanitari specifici vanno aggiunti quando i dataset ufficiali sono
abilitati e normalizzati.
"""

from utils_paths import get_configured_path, ensure_project_folders
from utils_io import read_table
from utils_plots import save_bar_chart


def main():
    ensure_project_folders()
    inventory_path = get_configured_path("outputs_tables") / "processed_dataset_inventory.csv"
    figures_root = get_configured_path("outputs_figures")
    if not inventory_path.exists():
        print("No inventory table found. Run src/05_build_indicators.py first.")
        return
    df = read_table(inventory_path)
    if df.empty or "rows" not in df.columns:
        print("Inventory table is empty or incomplete.")
        return
    save_bar_chart(
        df=df,
        x_col="dataset_path",
        y_col="rows",
        output_path=figures_root / "processed_dataset_rows.png",
        title="Rows by processed dataset",
    )
    print("Chart written to outputs/figures")


if __name__ == "__main__":
    main()
