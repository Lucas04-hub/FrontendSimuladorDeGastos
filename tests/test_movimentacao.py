from datetime import date
from decimal import Decimal

from financeiro.movimentacao import Movimentacao, TipoMovimentacao


def test_criar_movimentacao_valida():

    movimentacao = Movimentacao(
        descricao="Salário",
        valor=Decimal("3000.00"),
        tipo=TipoMovimentacao.ENTRADA,
        categoria="Trabalho",
        data=date(2026, 11, 24)
    )

    assert movimentacao.descricao == "Salário"
    assert movimentacao.valor == Decimal("3000.00")
    assert movimentacao.tipo == TipoMovimentacao.ENTRADA
    assert movimentacao.categoria == "Trabalho"
    assert movimentacao.data == date(2026, 11, 24)

def test_rejeitar_descricao_vazia():

    import pytest

    with pytest.raises(ValueError):
        Movimentacao(
            descricao="   ",
            valor=Decimal("100.00"),
            tipo=TipoMovimentacao.ENTRADA,
            categoria="Trabalho",
            data=date(2026, 11, 24)
        )

def test_rejeitar_valor_zero():

    import pytest

    with pytest.raises(ValueError):
        Movimentacao(
            descricao="Compra",
            valor=Decimal("0.00"),
            tipo=TipoMovimentacao.SAIDA,
            categoria="Alimentação",
            data=date(2026, 11, 24)
        )

def test_rejeitar_valor_negativo():

    import pytest

    with pytest.raises(ValueError):
        Movimentacao(
            descricao="Compra",
            valor=Decimal("-50.00"),
            tipo=TipoMovimentacao.SAIDA,
            categoria="Alimentação",
            data=date(2026, 11, 24)
        )

def test_rejeitar_categoria_vazia():

    import pytest

    with pytest.raises(ValueError):
        Movimentacao(
            descricao="Compra",
            valor=Decimal("50.00"),
            tipo=TipoMovimentacao.SAIDA,
            categoria="   ",
            data=date(2026, 11, 24)
        )

def test_rejeitar_tipo_invalido():

    import pytest

    with pytest.raises(TypeError):
        Movimentacao(
            descricao="Compra",
            valor=Decimal("50.00"),
            tipo="transferencia",
            categoria="Alimentação",
            data=date(2026, 11, 24)
        )

def test_rejeitar_data_invalida():

    import pytest

    with pytest.raises(TypeError):
        Movimentacao(
            descricao="Compra",
            valor=Decimal("50.00"),
            tipo=TipoMovimentacao.SAIDA,
            categoria="Alimentação",
            data="24/11/2026"
        )

def test_rejeitar_descricao_com_tipo_invalido():

    import pytest

    with pytest.raises(TypeError):
        Movimentacao(
            descricao=123,
            valor=Decimal("50.00"),
            tipo=TipoMovimentacao.SAIDA,
            categoria="Alimentação",
            data=date(2026, 11, 24)
        )

def test_rejeitar_categoria_com_tipo_invalido():

    import pytest

    with pytest.raises(TypeError):
        Movimentacao(
            descricao="Compra",
            valor=Decimal("50.00"),
            tipo=TipoMovimentacao.SAIDA,
            categoria=123,
            data=date(2026, 11, 24)
        )

def test_rejeitar_valor_com_tipo_invalido():

    import pytest

    with pytest.raises(TypeError):
        Movimentacao(
            descricao="Compra",
            valor=50.00,
            tipo=TipoMovimentacao.SAIDA,
            categoria="Alimentação",
            data=date(2026, 11, 24)
        )

def test_rejeitar_valor_nao_finito():

    import pytest

    with pytest.raises(ValueError):
        Movimentacao(
            descricao="Compra",
            valor=Decimal("NaN"),
            tipo=TipoMovimentacao.SAIDA,
            categoria="Alimentação",
            data=date(2026, 11, 24)
        )