from pathlib import Path
import os

BASE_DIR: Path = Path(__file__).resolve().parent
BACKUPS_DIR: Path = BASE_DIR / "backups"
DATA_DIR: Path = BASE_DIR / "data"
EXPORTS_DIR: Path = BASE_DIR / "exports"
DB_PATH: Path = DATA_DIR / "livraria.db"


def inicializar_estrutura_diretorios() -> None:
    for diretorio in (BACKUPS_DIR, DATA_DIR, EXPORTS_DIR):
        os.makedirs(diretorio, exist_ok=True)


