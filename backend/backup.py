from datetime import datetime
from pathlib import Path
import shutil

try:
    from .config import DB_PATH, BACKUPS_DIR, inicializar_estrutura_diretorios
except ImportError:
    from config import DB_PATH, BACKUPS_DIR, inicializar_estrutura_diretorios


def criar_backup() -> Path | None:
    inicializar_estrutura_diretorios()

    if not DB_PATH.exists():
        return None

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    destino = BACKUPS_DIR / f"backup_livraria_{timestamp}.db"
    shutil.copy2(DB_PATH, destino)
    return destino


def limpar_backups_antigos(max_arquivos: int = 5) -> list[Path]:
    inicializar_estrutura_diretorios()
    backups = sorted(
        BACKUPS_DIR.glob("backup_livraria_*.db"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    para_manter = backups[:max_arquivos]
    para_remover = backups[max_arquivos:]

    for caminho in para_remover:
        try:
            caminho.unlink()
        except FileNotFoundError:
            pass

    return para_manter


