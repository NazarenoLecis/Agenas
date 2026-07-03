"""
Utility per gestire i percorsi del progetto.
"""

from pathlib import Path
import yaml


def get_project_root():
    return Path(__file__).resolve().parents[1]


def load_yaml_file(path):
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    with path.open("r", encoding="utf-8") as file:
        data = yaml.safe_load(file)
    return data if data is not None else {}


def get_paths_config():
    return load_yaml_file(get_project_root() / "config" / "paths.yml")


def get_folder_path(folder_key):
    root = get_project_root()
    folders = get_paths_config().get("folders", {})
    if folder_key not in folders:
        raise KeyError(f"Missing folder key: {folder_key}")
    return root / folders[folder_key]


def ensure_folder(path):
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def ensure_project_folders():
    root = get_project_root()
    folders = get_paths_config().get("folders", {})
    for relative_path in folders.values():
        target = root / relative_path
        if str(target).endswith(".csv"):
            ensure_folder(target.parent)
        else:
            ensure_folder(target)
