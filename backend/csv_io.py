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


def exportar_livros_para_csv(caminho: Path | None = None) -> Path:
    if caminho is None:
        caminho = EXPORTS_DIR / "livros_exportados.csv"
    caminho.parent.mkdir(parents=True, exist_ok=True)

    campos = ["id", "titulo", "autor", "ano_publicacao", "preco"]
    linhas = listar_livros()

    with caminho.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()
        for linha in linhas:
            writer.writerow(linha)

    return caminho


def importar_livros_de_csv(caminho: Path) -> int:
    if not caminho.exists():
        raise FileNotFoundError(str(caminho))

    inseridos = 0
    # Um unico backup antes da operacao em massa
    criar_backup()
    with caminho.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            titulo = row.get("titulo", "")
            autor = row.get("autor", "")
            ano = row.get("ano_publicacao", "")
            preco = row.get("preco", "")
            adicionar_livro(titulo, autor, ano, preco, fazer_backup=False)
            inseridos += 1

    return inseridos


