from pathlib import Path

try:
    from .config import inicializar_estrutura_diretorios
    from .banco import criar_tabelas
    from .livros import (
        adicionar_livro,
        listar_livros,
        atualizar_preco,
        remover_livro,
        buscar_por_autor,
    )
    from .csv_io import exportar_livros_para_csv, importar_livros_de_csv
    from .backup import criar_backup
except ImportError:
    from config import inicializar_estrutura_diretorios
    from banco import criar_tabelas
    from livros import (
        adicionar_livro,
        listar_livros,
        atualizar_preco,
        remover_livro,
        buscar_por_autor,
    )
    from csv_io import exportar_livros_para_csv, importar_livros_de_csv
    from backup import criar_backup


def exibir_menu() -> None:
    print("1. Adicionar novo livro")
    print("2. Exibir todos os livros")
    print("3. Atualizar preço de um livro")
    print("4. Remover um livro")
    print("5. Buscar livros por autor")
    print("6. Exportar dados para CSV")
    print("7. Importar dados de CSV")
    print("8. Fazer backup do banco de dados")
    print("9. Sair")


def pausar() -> None:
    try:
        input("\nPressione Enter para continuar...")
    except EOFError:
        pass


def executar_menu() -> None:
    inicializar_estrutura_diretorios()
    criar_tabelas()

    while True:
        print("\n===== LIVRARIA BERNA - MENU =====")
        exibir_menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            try:
                titulo = input("Título: ").strip()
                autor = input("Autor: ").strip()
                ano = input("Ano de publicação: ").strip()
                preco = input("Preço: ").strip()
                novo_id = adicionar_livro(titulo, autor, ano, preco)
                print(f"Livro inserido com id {novo_id}.")
            except Exception as exc:
                print(f"Erro: {exc}")
            pausar()

        elif opcao == "2":
            livros = listar_livros()
            if not livros:
                print("Nenhum livro cadastrado.")
            else:
                print("\nID | Título | Autor | Ano | Preço")
                for l in livros:
                    print(f"{l['id']} | {l['titulo']} | {l['autor']} | {l['ano_publicacao']} | {l['preco']}")
            pausar()

        elif opcao == "3":
            try:
                id_livro = input("ID do livro: ").strip()
                novo_preco = input("Novo preço: ").strip()
                ok = atualizar_preco(id_livro, novo_preco)
                if ok:
                    print("Preço atualizado com sucesso.")
                else:
                    print("Livro não encontrado.")
            except Exception as exc:
                print(f"Erro: {exc}")
            pausar()

        elif opcao == "4":
            try:
                id_livro = input("ID do livro: ").strip()
                ok = remover_livro(id_livro)
                if ok:
                    print("Livro removido com sucesso.")
                else:
                    print("Livro não encontrado.")
            except Exception as exc:
                print(f"Erro: {exc}")
            pausar()

        elif opcao == "5":
            try:
                autor = input("Autor (termo de busca): ").strip()
                achados = buscar_por_autor(autor)
                if not achados:
                    print("Nenhum livro encontrado para este autor.")
                else:
                    print("\nID | Título | Autor | Ano | Preço")
                    for l in achados:
                        print(f"{l['id']} | {l['titulo']} | {l['autor']} | {l['ano_publicacao']} | {l['preco']}")
            except Exception as exc:
                print(f"Erro: {exc}")
            pausar()

        elif opcao == "6":
            try:
                caminho = exportar_livros_para_csv()
                print(f"Exportado para: {caminho}")
            except Exception as exc:
                print(f"Erro ao exportar: {exc}")
            pausar()

        elif opcao == "7":
            try:
                caminho_str = input("Caminho do CSV para importar: ").strip()
                inseridos = importar_livros_de_csv(Path(caminho_str))
                print(f"Registros inseridos: {inseridos}")
            except Exception as exc:
                print(f"Erro ao importar: {exc}")
            pausar()

        elif opcao == "8":
            try:
                arquivo = criar_backup()
                if arquivo:
                    print(f"Backup criado em: {arquivo}")
                else:
                    print("Nenhum banco para copiar.")
            except Exception as exc:
                print(f"Erro ao criar backup: {exc}")
            pausar()

        elif opcao == "9":
            print("Saindo...")
            break

        else:
            print("Opção inválida. Tente novamente.")


def main() -> None:
    executar_menu()


if __name__ == "__main__":
    main()


