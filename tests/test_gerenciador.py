import json
import pytest

from datetime import date
from decimal import Decimal

from financeiro.gerenciador import GerenciadorFinanceiro
from financeiro.movimentacao import Movimentacao, TipoMovimentacao


def test_iniciar_gerenciador_vazio(tmp_path):

    gerenciador = GerenciadorFinanceiro(
        tmp_path / "movimentacoes.json"
    )

    assert gerenciador.listar() == []


def test_adicionar_movimentacao_valida(tmp_path):

    gerenciador = GerenciadorFinanceiro(
        tmp_path / "movimentacoes.json"
    )

    movimentacao = Movimentacao(
        descricao="Salário",
        valor=Decimal("3000.00"),
        tipo=TipoMovimentacao.ENTRADA,
        categoria="Trabalho",
        data=date(2026, 11, 24)
    )

    gerenciador.adicionar(movimentacao)

    assert len(gerenciador.listar()) == 1
    assert gerenciador.listar()[0].descricao == "Salário"

def test_rejeitar_movimentacao_invalida(tmp_path):

    import pytest

    gerenciador = GerenciadorFinanceiro(
        tmp_path / "movimentacoes.json"
    )

    with pytest.raises(TypeError):
        gerenciador.adicionar("Movimentação inválida")

def test_listar_movimentacoes(tmp_path):

    gerenciador = GerenciadorFinanceiro(
        tmp_path / "movimentacoes.json"
    )

    movimentacao1 = Movimentacao(
        descricao="Salário",
        valor=Decimal("3000.00"),
        tipo=TipoMovimentacao.ENTRADA,
        categoria="Trabalho",
        data=date(2026, 11, 24)
    )

    movimentacao2 = Movimentacao(
        descricao="Mercado",
        valor=Decimal("150.00"),
        tipo=TipoMovimentacao.SAIDA,
        categoria="Alimentação",
        data=date(2026, 11, 24)
    )

    gerenciador.adicionar(movimentacao1)
    gerenciador.adicionar(movimentacao2)

    movimentacoes = gerenciador.listar()

    assert len(movimentacoes) == 2
    assert movimentacoes[0].descricao == "Salário"
    assert movimentacoes[1].descricao == "Mercado"

def test_remover_movimentacao_existente(tmp_path):

    gerenciador = GerenciadorFinanceiro(
        tmp_path / "movimentacoes.json"
    )

    movimentacao = Movimentacao(
        descricao="Compra de mercado",
        valor=Decimal("150.00"),
        tipo=TipoMovimentacao.SAIDA,
        categoria="Alimentação",
        data=date(2026, 11, 24),
        id=1
    )

    gerenciador.adicionar(movimentacao)

    resultado = gerenciador.remover(1)

    assert resultado is True
    assert gerenciador.listar() == []

def test_rejeitar_remocao_de_movimentacao_inexistente(tmp_path):

    import pytest

    gerenciador = GerenciadorFinanceiro(
        tmp_path / "movimentacoes.json"
    )

    with pytest.raises(ValueError):
        gerenciador.remover(999)

def test_atualizar_movimentacao_existente(tmp_path):

    gerenciador = GerenciadorFinanceiro(
        tmp_path / "movimentacoes.json"
    )

    movimentacao_antiga = Movimentacao(
        descricao="Compra de mercado",
        valor=Decimal("150.00"),
        tipo=TipoMovimentacao.SAIDA,
        categoria="Alimentação",
        data=date(2026, 11, 24),
        id=1
    )

    movimentacao_nova = Movimentacao(
        descricao="Compra de mercado atualizada",
        valor=Decimal("200.00"),
        tipo=TipoMovimentacao.SAIDA,
        categoria="Alimentação",
        data=date(2026, 11, 24)
    )

    gerenciador.adicionar(movimentacao_antiga)

    resultado = gerenciador.atualizar(1, movimentacao_nova)

    assert resultado is True
    assert gerenciador.listar()[0].descricao == "Compra de mercado atualizada"
    assert gerenciador.listar()[0].valor == Decimal("200.00")
    assert gerenciador.listar()[0].id == 1

def test_rejeitar_atualizacao_com_movimentacao_invalida(tmp_path):

    import pytest

    gerenciador = GerenciadorFinanceiro(
        tmp_path / "movimentacoes.json"
    )

    with pytest.raises(TypeError):
        gerenciador.atualizar(1, "Movimentação inválida")

def test_rejeitar_atualizacao_de_movimentacao_inexistente(tmp_path):

    import pytest

    gerenciador = GerenciadorFinanceiro(
        tmp_path / "movimentacoes.json"
    )

    movimentacao = Movimentacao(
        descricao="Compra",
        valor=Decimal("50.00"),
        tipo=TipoMovimentacao.SAIDA,
        categoria="Alimentação",
        data=date(2026, 11, 24)
    )

    with pytest.raises(ValueError):
        gerenciador.atualizar(999, movimentacao)

def test_calcular_total_entradas(tmp_path):

    gerenciador = GerenciadorFinanceiro(
        tmp_path / "movimentacoes.json"
    )

    movimentacao1 = Movimentacao(
        descricao="Salário",
        valor=Decimal("3000.00"),
        tipo=TipoMovimentacao.ENTRADA,
        categoria="Trabalho",
        data=date(2026, 11, 24)
    )

    movimentacao2 = Movimentacao(
        descricao="Freelance",
        valor=Decimal("1000.00"),
        tipo=TipoMovimentacao.ENTRADA,
        categoria="Serviços",
        data=date(2026, 11, 24)
    )

    movimentacao3 = Movimentacao(
        descricao="Mercado",
        valor=Decimal("150.00"),
        tipo=TipoMovimentacao.SAIDA,
        categoria="Alimentação",
        data=date(2026, 11, 24)
    )

    gerenciador.adicionar(movimentacao1)
    gerenciador.adicionar(movimentacao2)
    gerenciador.adicionar(movimentacao3)

    total = gerenciador.calcular_total_entradas()

    assert total == Decimal("4000.00")

def test_calcular_total_saidas(tmp_path):

    gerenciador = GerenciadorFinanceiro(
        tmp_path / "movimentacoes.json"
    )

    movimentacao1 = Movimentacao(
        descricao="Mercado",
        valor=Decimal("150.00"),
        tipo=TipoMovimentacao.SAIDA,
        categoria="Alimentação",
        data=date(2026, 11, 24)
    )

    movimentacao2 = Movimentacao(
        descricao="Internet",
        valor=Decimal("100.00"),
        tipo=TipoMovimentacao.SAIDA,
        categoria="Contas",
        data=date(2026, 11, 24)
    )

    movimentacao3 = Movimentacao(
        descricao="Salário",
        valor=Decimal("3000.00"),
        tipo=TipoMovimentacao.ENTRADA,
        categoria="Trabalho",
        data=date(2026, 11, 24)
    )

    gerenciador.adicionar(movimentacao1)
    gerenciador.adicionar(movimentacao2)
    gerenciador.adicionar(movimentacao3)

    total = gerenciador.calcular_total_saidas()

    assert total == Decimal("250.00")

def test_calcular_saldo(tmp_path):

    gerenciador = GerenciadorFinanceiro(
        tmp_path / "movimentacoes.json"
    )

    movimentacao1 = Movimentacao(
        descricao="Salário",
        valor=Decimal("3000.00"),
        tipo=TipoMovimentacao.ENTRADA,
        categoria="Trabalho",
        data=date(2026, 11, 24)
    )

    movimentacao2 = Movimentacao(
        descricao="Mercado",
        valor=Decimal("500.00"),
        tipo=TipoMovimentacao.SAIDA,
        categoria="Alimentação",
        data=date(2026, 11, 24)
    )

    movimentacao3 = Movimentacao(
        descricao="Internet",
        valor=Decimal("100.00"),
        tipo=TipoMovimentacao.SAIDA,
        categoria="Contas",
        data=date(2026, 11, 24)
    )

    gerenciador.adicionar(movimentacao1)
    gerenciador.adicionar(movimentacao2)
    gerenciador.adicionar(movimentacao3)

    saldo = gerenciador.calcular_saldo()

    assert saldo == Decimal("2400.00")

def test_salvar_movimentacoes_json(tmp_path):

    caminho_arquivo = tmp_path / "movimentacoes.json"

    gerenciador = GerenciadorFinanceiro(caminho_arquivo)

    movimentacao = Movimentacao(
        descricao="Salário",
        valor=Decimal("3000.00"),
        tipo=TipoMovimentacao.ENTRADA,
        categoria="Trabalho",
        data=date(2026, 11, 24),
        id=1
    )

    gerenciador.adicionar(movimentacao)

    with caminho_arquivo.open("r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)

    assert len(dados) == 1
    assert dados[0]["descricao"] == "Salário"
    assert dados[0]["valor"] == "3000.00"
    assert dados[0]["tipo"] == "entrada"
    assert dados[0]["categoria"] == "Trabalho"
    assert dados[0]["id"] == 1

def test_carregar_movimentacoes_json(tmp_path):

    caminho_arquivo = tmp_path / "movimentacoes.json"

    dados = [
        {
            "descricao": "Salário",
            "valor": "3000.00",
            "tipo": "entrada",
            "categoria": "Trabalho",
            "data": "2026-11-24",
            "id": 1
        }
    ]

    with caminho_arquivo.open("w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=4)

    gerenciador = GerenciadorFinanceiro(caminho_arquivo)

    movimentacoes = gerenciador.listar()

    assert len(movimentacoes) == 1
    assert movimentacoes[0].descricao == "Salário"
    assert movimentacoes[0].valor == Decimal("3000.00")
    assert movimentacoes[0].tipo == TipoMovimentacao.ENTRADA
    assert movimentacoes[0].categoria == "Trabalho"
    assert movimentacoes[0].data == date(2026, 11, 24)
    assert movimentacoes[0].id == 1

def test_listar_retorna_copia_da_lista(tmp_path):

    gerenciador = GerenciadorFinanceiro(
        tmp_path / "movimentacoes.json"
    )

    movimentacao = Movimentacao(
        descricao="Salário",
        valor=Decimal("3000.00"),
        tipo=TipoMovimentacao.ENTRADA,
        categoria="Trabalho",
        data=date(2026, 11, 24),
        id=1
    )

    gerenciador.adicionar(movimentacao)

    movimentacoes = gerenciador.listar()

    movimentacoes.clear()

    assert len(gerenciador.listar()) == 1