from typing import Any

try:
    from .banco import obter_conexao
    from .backup import criar_backup
    from .validacao import (
        validar_titulo,
        validar_autor,
        validar_ano_publicacao,
        validar_preco,
    )
except ImportError:
    from banco import obter_conexao
    from backup import criar_backup
    from validacao import (
        validar_titulo,
        validar_autor,
        validar_ano_publicacao,
        validar_preco,
    )


def adicionar_livro(titulo: str, autor: str, ano_publicacao: int | str, preco: float | str, fazer_backup: bool = True) -> int:
    if fazer_backup:
        criar_backup()
    titulo_ok = validar_titulo(titulo)
    autor_ok = validar_autor(autor)
    ano_ok = validar_ano_publicacao(ano_publicacao)
    preco_ok = validar_preco(preco)

    with obter_conexao() as conn:
        cur = conn.execute(
            "INSERT INTO livros (titulo, autor, ano_publicacao, preco) VALUES (?, ?, ?, ?)",
            (titulo_ok, autor_ok, ano_ok, preco_ok),
        )
        conn.commit()
        return int(cur.lastrowid)


def listar_livros() -> list[dict[str, Any]]:
    with obter_conexao() as conn:
        rows = conn.execute("SELECT id, titulo, autor, ano_publicacao, preco FROM livros ORDER BY id").fetchall()
        return [dict(r) for r in rows]


def atualizar_preco(id_livro: int | str, novo_preco: float | str) -> bool:
    criar_backup()
    try:
        id_ok = int(id_livro)
    except (TypeError, ValueError) as exc:
        raise ValueError("id invalido") from exc
    preco_ok = validar_preco(novo_preco)

    with obter_conexao() as conn:
        cur = conn.execute(
            "UPDATE livros SET preco = ? WHERE id = ?",
            (preco_ok, id_ok),
        )
        conn.commit()
        return cur.rowcount > 0


def remover_livro(id_livro: int | str) -> bool:
    criar_backup()
    try:
        id_ok = int(id_livro)
    except (TypeError, ValueError) as exc:
        raise ValueError("id invalido") from exc

    with obter_conexao() as conn:
        cur = conn.execute("DELETE FROM livros WHERE id = ?", (id_ok,))
        conn.commit()
        return cur.rowcount > 0


def buscar_por_autor(autor: str) -> list[dict[str, Any]]:
    autor_ok = validar_autor(autor)
    with obter_conexao() as conn:
        rows = conn.execute(
            "SELECT id, titulo, autor, ano_publicacao, preco FROM livros WHERE autor LIKE ? ORDER BY id",
            (f"%{autor_ok}%",),
        ).fetchall()
        return [dict(r) for r in rows]


