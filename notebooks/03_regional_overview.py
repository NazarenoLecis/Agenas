# %%
# Regional overview
#
# Questo notebook in formato Python usa le celle Jupyter percent.
# Aprirlo con VS Code, Jupyter o editor compatibili con celle # %%.

from pathlib import Path
import pandas as pd

ROOT = Path.cwd()
inventory_path = ROOT / "outputs" / "tables" / "processed_dataset_inventory.csv"

if inventory_path.exists():
    inventory = pd.read_csv(inventory_path)
else:
    inventory = pd.DataFrame()

inventory

# %%
if inventory.empty:
    print("Run the pipeline before this notebook.")
else:
    display(inventory.sort_values("rows", ascending=False).head(20))
