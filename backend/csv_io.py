import csv
from pathlib import Path

try:
    from .config import EXPORTS_DIR
    from .backup import criar_backup
    from .livros import adicionar_livro, listar_livros
except ImportError:
    from config import EXPORTS_DIR
    from backup import criar_backup
    from livros import adicionar_livro, listar_livros


def exportar_livros_para_csv(path: Path | None = None) -> Path:
    if path is None:
        path = EXPORTS_DIR / "livros_exportados.csv"
    path.parent.mkdir(parents=True, exist_ok=True)

    campos = ["id", "titulo", "autor", "ano_publicacao", "preco"]
    linhas = listar_livros()

    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()
        for linha in linhas:
            writer.writerow(linha)

    return path


def importar_livros_de_csv(path: Path) -> int:
    if not path.exists():
        raise FileNotFoundError(str(path))

    inseridos = 0
    criar_backup()
    with path.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            titulo = row.get("titulo", "")
            autor = row.get("autor", "")
            ano = row.get("ano_publicacao", "")
            preco = row.get("preco", "")
            adicionar_livro(titulo, autor, ano, preco, fazer_backup=False)
            inseridos += 1

    return inseridos


