import sys
from pathlib import Path
from datetime import date
from decimal import Decimal, InvalidOperation

from flask import Flask, render_template, jsonify, request


# 1. CONFIGURAÇÃO DOS CAMINHOS

BASE_DIR = Path(__file__).resolve().parent

SRC_DIR = BASE_DIR / "src"

sys.path.insert(0, str(SRC_DIR))


# 2. IMPORTAÇÃO DO BACKEND

from financeiro.gerenciador import GerenciadorFinanceiro

from financeiro.movimentacao import (
    Movimentacao,
    TipoMovimentacao
)

# 3. CONFIGURAÇÃO DO FLASK

app = Flask(
    __name__,
    template_folder="frontend/templates",
    static_folder="frontend/static"
)


# 4. INSTÂNCIA DO GERENCIADOR

gerenciador = GerenciadorFinanceiro(
    arquivo=BASE_DIR / "data" / "movimentacoes.json"
)


# 5. ROTA PRINCIPAL

@app.route("/")
def inicio():
    return render_template("index.html")


# 6. ROTA PARA LISTAR MOVIMENTAÇÕES

@app.route("/api/movimentacoes")
def listar_movimentacoes():

    movimentacoes = gerenciador.listar()

    dados = []

    for movimentacao in movimentacoes:
        dados.append({
            "id": movimentacao.id,
            "descricao": movimentacao.descricao,
            "valor": str(movimentacao.valor),
            "tipo": movimentacao.tipo.value,
            "categoria": movimentacao.categoria,
            "data": movimentacao.data.isoformat()
        })

    return jsonify(dados)

# 7. ROTA PARA CADASTRAR MOVIMENTAÇÕES

@app.route("/api/movimentacoes", methods=["POST"])
def cadastrar_movimentacao():

    dados = request.get_json(silent=True)

    if not isinstance(dados, dict):
        return jsonify({
            "erro": "Os dados enviados são inválidos."
        }), 400

    campos_obrigatorios = [
        "descricao",
        "valor",
        "tipo",
        "categoria",
        "data"
    ]

    for campo in campos_obrigatorios:
        if campo not in dados:
            return jsonify({
                "erro": f"O campo {campo} é obrigatório."
            }), 400

    try:
        valor = Decimal(str(dados["valor"]))

        tipo = TipoMovimentacao(dados["tipo"])

        data_movimentacao = date.fromisoformat(dados["data"])

        movimentacoes_existentes = gerenciador.listar()

        novo_id = max(
            (m.id for m in movimentacoes_existentes if m.id is not None),
            default=0
        ) + 1

        movimentacao = Movimentacao(
            descricao=dados["descricao"],
            valor=valor,
            tipo=tipo,
            categoria=dados["categoria"],
            data=data_movimentacao,
            id=novo_id
        )

        gerenciador.adicionar(movimentacao)

        return jsonify({
            "mensagem": "Movimentação cadastrada com sucesso!",
            "movimentacao": {
                "id": movimentacao.id,
                "descricao": movimentacao.descricao,
                "valor": str(movimentacao.valor),
                "tipo": movimentacao.tipo.value,
                "categoria": movimentacao.categoria,
                "data": movimentacao.data.isoformat()
            }
        }), 201

    except (ValueError, TypeError, InvalidOperation) as erro:

        return jsonify({
            "erro": str(erro)
        }), 400

# 8. ROTA PARA EXCLUIR MOVIMENTAÇÕES

@app.route("/api/movimentacoes/<int:identificador>", methods=["DELETE"])
def excluir_movimentacao(identificador):

    try:
        gerenciador.remover(identificador)

        return jsonify({
            "mensagem": "Movimentação excluída com sucesso!"
        }), 200

    except ValueError as erro:

        return jsonify({
            "erro": str(erro)
        }), 404

@app.route("/api/movimentacoes/<int:identificador>", methods=["PUT"])
def atualizar_movimentacao(identificador):

    dados = request.get_json(silent=True)

    if not isinstance(dados, dict):
        return jsonify({
            "erro": "Os dados enviados são inválidos."
        }), 400

    campos_obrigatorios = [
        "descricao",
        "valor",
        "tipo",
        "categoria",
        "data"
    ]

    for campo in campos_obrigatorios:
        if campo not in dados:
            return jsonify({
                "erro": f"O campo {campo} é obrigatório."
            }), 400

    try:

        valor = Decimal(str(dados["valor"]))

        tipo = TipoMovimentacao(dados["tipo"])

        data_movimentacao = date.fromisoformat(dados["data"])

        movimentacao = Movimentacao(
            descricao=dados["descricao"],
            valor=valor,
            tipo=tipo,
            categoria=dados["categoria"],
            data=data_movimentacao,
            id=identificador
        )

        gerenciador.atualizar(
            identificador,
            movimentacao
        )

        return jsonify({
            "mensagem": "Movimentação atualizada com sucesso!"
        }), 200

    except (ValueError, TypeError, InvalidOperation) as erro:

        return jsonify({
            "erro": str(erro)
        }), 400

# 10. EXECUÇÃO DO SERVIDOR

if __name__ == "__main__":
    app.run(debug=True)