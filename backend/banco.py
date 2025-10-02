import sqlite3
from sqlite3 import Connection

try:
    from .config import DB_PATH, inicializar_estrutura_diretorios
except ImportError:
    from config import DB_PATH, inicializar_estrutura_diretorios


def connectbd() -> Connection:
    inicializar_estrutura_diretorios()
    bd = sqlite3.connect(DB_PATH)
    bd.row_factory = sqlite3.Row
    return bd


def criar_tabelas() -> None:
    with connectbd() as bd:
        bd.execute(
            """
            CREATE TABLE IF NOT EXISTS livros (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                autor TEXT NOT NULL,
                ano_publicacao INTEGER NOT NULL,
                preco REAL NOT NULL
            )
            """
        )
        bd.commit()


