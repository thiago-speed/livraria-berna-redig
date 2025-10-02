try:
    from .config import inicializar_estrutura_diretorios
    from .banco import criar_tabelas
    from .api import app
except ImportError:
    # Execução direta: python3 main.py dentro de backend/
    from config import inicializar_estrutura_diretorios
    from banco import criar_tabelas
    from api import app


def main() -> None:
    # Inicializa backend (diretórios e tabelas) e inicia o servidor Flask
    inicializar_estrutura_diretorios()
    criar_tabelas()
    app.run(host="0.0.0.0", port=5000)


if __name__ == "__main__":
    main()


