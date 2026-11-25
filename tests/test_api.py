import app as modulo_app

from datetime import date
from decimal import Decimal

from financeiro.gerenciador import GerenciadorFinanceiro
from financeiro.movimentacao import Movimentacao, TipoMovimentacao


def test_listar_movimentacoes():

    cliente = modulo_app.app.test_client()

    resposta = cliente.get("/api/movimentacoes")

    assert resposta.status_code == 200
    assert resposta.content_type.startswith("application/json")
    assert isinstance(resposta.get_json(), list)

def test_cadastrar_movimentacao(monkeypatch, tmp_path):

    gerenciador_teste = GerenciadorFinanceiro(
        tmp_path / "movimentacoes.json"
    )

    monkeypatch.setattr(
        modulo_app,
        "gerenciador",
        gerenciador_teste
    )

    cliente = modulo_app.app.test_client()

    dados = {
        "descricao": "Salário",
        "valor": "3000.00",
        "tipo": "entrada",
        "categoria": "Trabalho",
        "data": "2026-11-24"
    }

    resposta = cliente.post(
        "/api/movimentacoes",
        json=dados
    )

    assert resposta.status_code == 201

    resultado = resposta.get_json()

    assert resultado["mensagem"] == "Movimentação cadastrada com sucesso!"
    assert resultado["movimentacao"]["descricao"] == "Salário"
    assert resultado["movimentacao"]["valor"] == "3000.00"
    assert resultado["movimentacao"]["tipo"] == "entrada"

def test_rejeitar_cadastro_com_dados_invalidos(monkeypatch, tmp_path):

    gerenciador_teste = GerenciadorFinanceiro(
        tmp_path / "movimentacoes.json"
    )

    monkeypatch.setattr(
        modulo_app,
        "gerenciador",
        gerenciador_teste
    )

    cliente = modulo_app.app.test_client()

    dados = {
        "descricao": "",
        "valor": "100.00",
        "tipo": "entrada",
        "categoria": "Trabalho",
        "data": "2026-11-24"
    }

    resposta = cliente.post(
        "/api/movimentacoes",
        json=dados
    )

    assert resposta.status_code == 400

    resultado = resposta.get_json()

    assert "erro" in resultado
    assert gerenciador_teste.listar() == []

def test_rejeitar_cadastro_sem_campo_obrigatorio(monkeypatch, tmp_path):

    gerenciador_teste = GerenciadorFinanceiro(
        tmp_path / "movimentacoes.json"
    )

    monkeypatch.setattr(
        modulo_app,
        "gerenciador",
        gerenciador_teste
    )

    cliente = modulo_app.app.test_client()

    dados = {
        "descricao": "Salário",
        "valor": "3000.00",
        "tipo": "entrada",
        "data": "2026-11-24"
    }

    resposta = cliente.post(
        "/api/movimentacoes",
        json=dados
    )

    assert resposta.status_code == 400

    resultado = resposta.get_json()

    assert "erro" in resultado
    assert "categoria" in resultado["erro"]
    assert gerenciador_teste.listar() == []

def test_rejeitar_tipo_de_movimentacao_invalido(monkeypatch, tmp_path):

    gerenciador_teste = GerenciadorFinanceiro(
        tmp_path / "movimentacoes.json"
    )

    monkeypatch.setattr(
        modulo_app,
        "gerenciador",
        gerenciador_teste
    )

    cliente = modulo_app.app.test_client()

    dados = {
        "descricao": "Salário",
        "valor": "3000.00",
        "tipo": "transferencia",
        "categoria": "Trabalho",
        "data": "2026-11-24"
    }

    resposta = cliente.post(
        "/api/movimentacoes",
        json=dados
    )

    assert resposta.status_code == 400

    resultado = resposta.get_json()

    assert "erro" in resultado
    assert gerenciador_teste.listar() == []

def test_rejeitar_valor_negativo(monkeypatch, tmp_path):

    gerenciador_teste = GerenciadorFinanceiro(
        tmp_path / "movimentacoes.json"
    )

    monkeypatch.setattr(
        modulo_app,
        "gerenciador",
        gerenciador_teste
    )

    cliente = modulo_app.app.test_client()

    dados = {
        "descricao": "Compra de mercado",
        "valor": "-150.00",
        "tipo": "saida",
        "categoria": "Alimentação",
        "data": "2026-11-24"
    }

    resposta = cliente.post(
        "/api/movimentacoes",
        json=dados
    )

    assert resposta.status_code == 400

    resultado = resposta.get_json()

    assert "erro" in resultado
    assert gerenciador_teste.listar() == []

def test_rejeitar_valor_zero(monkeypatch, tmp_path):

    gerenciador_teste = GerenciadorFinanceiro(
        tmp_path / "movimentacoes.json"
    )

    monkeypatch.setattr(
        modulo_app,
        "gerenciador",
        gerenciador_teste
    )

    cliente = modulo_app.app.test_client()

    dados = {
        "descricao": "Compra de mercado",
        "valor": "0.00",
        "tipo": "saida",
        "categoria": "Alimentação",
        "data": "2026-11-24"
    }

    resposta = cliente.post(
        "/api/movimentacoes",
        json=dados
    )

    assert resposta.status_code == 400

    resultado = resposta.get_json()

    assert "erro" in resultado
    assert gerenciador_teste.listar() == []

def test_rejeitar_data_invalida(monkeypatch, tmp_path):

    gerenciador_teste = GerenciadorFinanceiro(
        tmp_path / "movimentacoes.json"
    )

    monkeypatch.setattr(
        modulo_app,
        "gerenciador",
        gerenciador_teste
    )

    cliente = modulo_app.app.test_client()

    dados = {
        "descricao": "Compra de mercado",
        "valor": "150.00",
        "tipo": "saida",
        "categoria": "Alimentação",
        "data": "data-invalida"
    }

    resposta = cliente.post(
        "/api/movimentacoes",
        json=dados
    )

    assert resposta.status_code == 400

    resultado = resposta.get_json()

    assert "erro" in resultado
    assert gerenciador_teste.listar() == []

def test_rejeitar_dados_que_nao_sao_json_valido(monkeypatch, tmp_path):

    gerenciador_teste = GerenciadorFinanceiro(
        tmp_path / "movimentacoes.json"
    )

    monkeypatch.setattr(
        modulo_app,
        "gerenciador",
        gerenciador_teste
    )

    cliente = modulo_app.app.test_client()

    resposta = cliente.post(
        "/api/movimentacoes",
        data="isso nao e um json",
        content_type="text/plain"
    )

    assert resposta.status_code == 400

    resultado = resposta.get_json()

    assert "erro" in resultado
    assert gerenciador_teste.listar() == []

def test_atualizar_movimentacao(monkeypatch, tmp_path):

    gerenciador_teste = GerenciadorFinanceiro(
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

    gerenciador_teste.adicionar(movimentacao)

    monkeypatch.setattr(
        modulo_app,
        "gerenciador",
        gerenciador_teste
    )

    cliente = modulo_app.app.test_client()

    dados = {
        "descricao": "Compra de mercado atualizada",
        "valor": "200.00",
        "tipo": "saida",
        "categoria": "Alimentação",
        "data": "2026-11-24"
    }

    resposta = cliente.put(
        "/api/movimentacoes/1",
        json=dados
    )

    assert resposta.status_code == 200

    resultado = resposta.get_json()

    assert resultado["mensagem"] == "Movimentação atualizada com sucesso!"

    movimentacao_atualizada = gerenciador_teste.listar()[0]

    assert movimentacao_atualizada.descricao == "Compra de mercado atualizada"
    assert movimentacao_atualizada.valor == Decimal("200.00")
    assert movimentacao_atualizada.id == 1

def test_atualizar_movimentacao_inexistente(monkeypatch, tmp_path):

    gerenciador_teste = GerenciadorFinanceiro(
        tmp_path / "movimentacoes.json"
    )

    monkeypatch.setattr(
        modulo_app,
        "gerenciador",
        gerenciador_teste
    )

    cliente = modulo_app.app.test_client()

    dados = {
        "descricao": "Conta de internet",
        "valor": "120.00",
        "tipo": "saida",
        "categoria": "Moradia",
        "data": "2026-11-24"
    }

    resposta = cliente.put(
        "/api/movimentacoes/999",
        json=dados
    )

    assert resposta.status_code == 400
    assert "erro" in resposta.get_json()
    assert gerenciador_teste.listar() == []

def test_excluir_movimentacao(monkeypatch, tmp_path):

    gerenciador_teste = GerenciadorFinanceiro(
        tmp_path / "movimentacoes.json"
    )

    movimentacao = Movimentacao(
        descricao="Conta de internet",
        valor=Decimal("120.00"),
        tipo=TipoMovimentacao.SAIDA,
        categoria="Moradia",
        data=date(2026, 11, 24),
        id=1
    )

    gerenciador_teste.adicionar(movimentacao)

    monkeypatch.setattr(
        modulo_app,
        "gerenciador",
        gerenciador_teste
    )

    cliente = modulo_app.app.test_client()

    resposta = cliente.delete("/api/movimentacoes/1")

    assert resposta.status_code == 200

    resultado = resposta.get_json()

    assert resultado["mensagem"] == "Movimentação excluída com sucesso!"
    assert gerenciador_teste.listar() == []

def test_excluir_movimentacao_inexistente(monkeypatch, tmp_path):

    gerenciador_teste = GerenciadorFinanceiro(
        tmp_path / "movimentacoes.json"
    )

    monkeypatch.setattr(
        modulo_app,
        "gerenciador",
        gerenciador_teste
    )

    cliente = modulo_app.app.test_client()

    resposta = cliente.delete("/api/movimentacoes/999")

    assert resposta.status_code == 404

    resultado = resposta.get_json()

    assert "erro" in resultado
    assert gerenciador_teste.listar() == []

def test_listar_movimentacoes_com_dados(monkeypatch, tmp_path):

    gerenciador_teste = GerenciadorFinanceiro(
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

    gerenciador_teste.adicionar(movimentacao)

    monkeypatch.setattr(
        modulo_app,
        "gerenciador",
        gerenciador_teste
    )

    cliente = modulo_app.app.test_client()

    resposta = cliente.get("/api/movimentacoes")

    assert resposta.status_code == 200

    resultado = resposta.get_json()

    assert len(resultado) == 1
    assert resultado[0]["id"] == 1
    assert resultado[0]["descricao"] == "Salário"
    assert resultado[0]["valor"] == "3000.00"
    assert resultado[0]["tipo"] == "entrada"
    assert resultado[0]["categoria"] == "Trabalho"
    assert resultado[0]["data"] == "2026-11-24"

def test_atualizar_movimentacao_sem_campo_obrigatorio(monkeypatch, tmp_path):

    gerenciador_teste = GerenciadorFinanceiro(
        tmp_path / "movimentacoes.json"
    )

    monkeypatch.setattr(
        modulo_app,
        "gerenciador",
        gerenciador_teste
    )

    cliente = modulo_app.app.test_client()

    dados = {
        "descricao": "Conta de internet",
        "valor": "120.00",
        "tipo": "saida",
        "data": "2026-11-24"
    }

    resposta = cliente.put(
        "/api/movimentacoes/1",
        json=dados
    )

    assert resposta.status_code == 400

    resultado = resposta.get_json()

    assert "erro" in resultado
    assert "categoria" in resultado["erro"]
    assert gerenciador_teste.listar() == []

def test_atualizar_movimentacao_com_valor_negativo(monkeypatch, tmp_path):

    gerenciador_teste = GerenciadorFinanceiro(
        tmp_path / "movimentacoes.json"
    )

    movimentacao = Movimentacao(
        descricao="Conta de internet",
        valor=Decimal("120.00"),
        tipo=TipoMovimentacao.SAIDA,
        categoria="Moradia",
        data=date(2026, 11, 24),
        id=1
    )

    gerenciador_teste.adicionar(movimentacao)

    monkeypatch.setattr(
        modulo_app,
        "gerenciador",
        gerenciador_teste
    )

    cliente = modulo_app.app.test_client()

    dados = {
        "descricao": "Conta de internet atualizada",
        "valor": "-200.00",
        "tipo": "saida",
        "categoria": "Moradia",
        "data": "2026-11-24"
    }

    resposta = cliente.put(
        "/api/movimentacoes/1",
        json=dados
    )

    assert resposta.status_code == 400

    resultado = resposta.get_json()

    assert "erro" in resultado

    movimentacao_atual = gerenciador_teste.listar()[0]

    assert movimentacao_atual.valor == Decimal("120.00")
    assert movimentacao_atual.descricao == "Conta de internet"