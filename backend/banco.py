import sqlite3
from sqlite3 import Connection

try:
    from .config import DB_PATH, inicializar_estrutura_diretorios
except ImportError:
    from config import DB_PATH, inicializar_estrutura_diretorios


def obter_conexao() -> Connection:
    inicializar_estrutura_diretorios()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def criar_tabelas() -> None:
    with obter_conexao() as conn:
        conn.execute(
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
        conn.commit()


