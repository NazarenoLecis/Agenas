"""
Utility DuckDB.

Il modulo crea un database locale a partire dai file CSV e Parquet presenti in
cartelle del progetto. Serve per interrogare molti dataset senza caricarli tutti
in memoria con pandas.
"""

from pathlib import Path
import duckdb


def connect_database(database_path):
    database_path = Path(database_path)
    database_path.parent.mkdir(parents=True, exist_ok=True)
    return duckdb.connect(str(database_path))


def safe_table_name(path):
    name = Path(path).stem.lower()
    cleaned = []
    for char in name:
        cleaned.append(char if char.isalnum() else "_")
    return "".join(cleaned).strip("_")


def register_file(connection, file_path, table_name=None):
    file_path = Path(file_path)
    table_name = table_name or safe_table_name(file_path)
    if file_path.suffix.lower() == ".csv":
        connection.execute(
            f"CREATE OR REPLACE VIEW {table_name} AS SELECT * FROM read_csv_auto(?)",
            [str(file_path)],
        )
    elif file_path.suffix.lower() == ".parquet":
        connection.execute(
            f"CREATE OR REPLACE VIEW {table_name} AS SELECT * FROM read_parquet(?)",
            [str(file_path)],
        )
    return table_name


def register_folder(connection, folder_path):
    folder_path = Path(folder_path)
    tables = []
    for file_path in list(folder_path.rglob("*.csv")) + list(folder_path.rglob("*.parquet")):
        tables.append(register_file(connection, file_path))
    return tables
