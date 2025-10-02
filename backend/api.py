from pathlib import Path
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

try:
    from .config import inicializar_estrutura_diretorios, EXPORTS_DIR
    from .banco import criar_tabelas
    from .livros import (
        adicionar_livro,
        listar_livros,
        atualizar_preco,
        remover_livro,
        buscar_por_autor,
    )
    from .csv_io import exportar_livros_para_csv, importar_livros_de_csv
    from .backup import criar_backup, limpar_backups_antigos
except ImportError:
    from config import inicializar_estrutura_diretorios, EXPORTS_DIR
    from banco import criar_tabelas
    from livros import (
        adicionar_livro,
        listar_livros,
        atualizar_preco,
        remover_livro,
        buscar_por_autor,
    )
    from csv_io import exportar_livros_para_csv, importar_livros_de_csv
    from backup import criar_backup, limpar_backups_antigos


app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False
CORS(app)

inicializar_estrutura_diretorios()
criar_tabelas()


def resposta_erro(mensagem: str, status: int = 400):
    return jsonify({"sucesso": False, "mensagem": mensagem}), status


@app.get("/livros")
def rota_listar_livros():
    dados = listar_livros()
    return jsonify({"sucesso": True, "dados": dados})


@app.post("/livros")
def rota_adicionar_livro():
    body = request.get_json(silent=True) or {}
    try:
        novo_id = adicionar_livro(
            body.get("titulo", ""),
            body.get("autor", ""),
            body.get("ano_publicacao", ""),
            body.get("preco", ""),
        )
        return jsonify({"sucesso": True, "id": novo_id}), 201
    except Exception as exc:
        return resposta_erro(str(exc), status=400)


@app.put("/livros/<int:id_livro>/preco")
def rota_atualizar_preco(id_livro: int):
    body = request.get_json(silent=True) or {}
    if "preco" not in body:
        return resposta_erro("preco obrigatorio", 400)
    try:
        ok = atualizar_preco(id_livro, body["preco"])
        if not ok:
            return resposta_erro("livro nao encontrado", 404)
        return jsonify({"sucesso": True})
    except Exception as exc:
        return resposta_erro(str(exc), status=400)


@app.delete("/livros/<int:id_livro>")
def rota_remover_livro(id_livro: int):
    try:
        ok = remover_livro(id_livro)
        if not ok:
            return resposta_erro("livro nao encontrado", 404)
        return jsonify({"sucesso": True})
    except Exception as exc:
        return resposta_erro(str(exc), status=400)


@app.get("/livros/buscar")
def rota_buscar_por_autor():
    autor = request.args.get("autor", "")
    if not autor:
        return resposta_erro("parametro 'autor' obrigatorio", 400)
    try:
        dados = buscar_por_autor(autor)
        return jsonify({"sucesso": True, "dados": dados})
    except Exception as exc:
        return resposta_erro(str(exc), status=400)


@app.get("/exportar")
def rota_exportar_csv():
    caminho = exportar_livros_para_csv()
    return send_file(caminho, as_attachment=True, download_name=caminho.name, mimetype="text/csv")


@app.post("/importar")
def rota_importar_csv():
    if "arquivo" in request.files:
        arquivo = request.files["arquivo"]
        if arquivo.filename == "":
            return resposta_erro("arquivo vazio", 400)
        EXPORTS_DIR.mkdir(parents=True, exist_ok=True)
        destino = EXPORTS_DIR / "import_temp.csv"
        arquivo.save(destino)
        try:
            inseridos = importar_livros_de_csv(destino)
        finally:
            try:
                destino.unlink(missing_ok=True)
            except Exception:
                pass
        return jsonify({"sucesso": True, "inseridos": inseridos})

    body = request.get_json(silent=True) or {}
    caminho_str = body.get("caminho")
    if not caminho_str:
        return resposta_erro("nenhum arquivo enviado ou 'caminho' informado", 400)
    caminho = Path(caminho_str)
    try:
        inseridos = importar_livros_de_csv(caminho)
        return jsonify({"sucesso": True, "inseridos": inseridos})
    except Exception as exc:
        return resposta_erro(str(exc), 400)


@app.get("/backup")
def rota_criar_backup():
    caminho = criar_backup()
    if not caminho:
        return jsonify({"sucesso": True, "mensagem": "nenhum banco para copiar"})
    return jsonify({"sucesso": True, "arquivo": str(caminho)})


@app.post("/backups/limpar")
def rota_limpar_backups():
    try:
        max_str = request.args.get("max", "5")
        max_int = int(max_str)
    except ValueError:
        return resposta_erro("parametro 'max' invalido", 400)
    mantidos = limpar_backups_antigos(max_int)
    return jsonify({"sucesso": True, "mantidos": [str(p) for p in mantidos]})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


