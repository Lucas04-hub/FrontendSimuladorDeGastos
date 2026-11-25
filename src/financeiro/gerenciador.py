import json
from pathlib import Path
from decimal import Decimal
from datetime import date

from financeiro.movimentacao import (
    Movimentacao,
    TipoMovimentacao
)


class GerenciadorFinanceiro:

    def __init__(self, arquivo=None):
        self._movimentacoes = []

        if arquivo is None:
            self._arquivo = Path("data/movimentacoes.json")
        else:
            self._arquivo = Path(arquivo)

        self._arquivo.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        self.carregar()

    def adicionar(self, movimentacao):
        if not isinstance(movimentacao, Movimentacao):
            raise TypeError("É necessário fornecer uma movimentação válida.")

        self._movimentacoes.append(movimentacao)
        self.salvar()

    def listar(self):
        return self._movimentacoes.copy()
    
    def remover(self, identificador):
        """
        Remove uma movimentação pelo seu ID.
        """

        for movimentacao in self._movimentacoes:

            if movimentacao.id == identificador:

                self._movimentacoes.remove(movimentacao)

                self.salvar()

                return True

        raise ValueError("Movimentação não encontrada.")
    
    def atualizar(self, identificador, nova_movimentacao):

        # Verifica se o objeto recebido é uma movimentação válida.
        if not isinstance(nova_movimentacao, Movimentacao):
            raise TypeError("É necessário fornecer uma movimentação válida.")

        # Procura a movimentação pelo ID.
        for indice, movimentacao in enumerate(self._movimentacoes):

            if movimentacao.id == identificador:

                # Mantém o ID original da movimentação.
                nova_movimentacao.id = identificador

                # Substitui a movimentação antiga pela nova.
                self._movimentacoes[indice] = nova_movimentacao

                # Salva as alterações no arquivo JSON.
                self.salvar()

                return True

        raise ValueError("Movimentação não encontrada.")


    def calcular_total_entradas(self):
        return sum(
            (
                m.valor
                for m in self._movimentacoes
                if m.tipo == TipoMovimentacao.ENTRADA
            ),
            Decimal("0.00")
        )

    def calcular_total_saidas(self):
        return sum(
            (
                m.valor
                for m in self._movimentacoes
                if m.tipo == TipoMovimentacao.SAIDA
            ),
            Decimal("0.00")
        )

    def calcular_saldo(self):
        return (
            self.calcular_total_entradas()
            - self.calcular_total_saidas()
        )

    def salvar(self):
        dados = []

        for movimentacao in self._movimentacoes:
            dados.append({
                "descricao": movimentacao.descricao,
                "valor": str(movimentacao.valor),
                "tipo": movimentacao.tipo.value,
                "categoria": movimentacao.categoria,
                "data": movimentacao.data.isoformat(),
                "id": movimentacao.id
            })

        with self._arquivo.open("w", encoding="utf-8") as arquivo:
            json.dump(
                dados,
                arquivo,
                ensure_ascii=False,
                indent=4
            )

    def carregar(self):
        if not self._arquivo.exists():
            self._movimentacoes = []
            return

        with self._arquivo.open("r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)

        self._movimentacoes = []

        for item in dados:
            movimentacao = Movimentacao(
                descricao=item["descricao"],
                valor=Decimal(item["valor"]),
                tipo=TipoMovimentacao(item["tipo"]),
                categoria=item["categoria"],
                data=date.fromisoformat(item["data"]),
                id=item.get("id")
            )

            self._movimentacoes.append(movimentacao)
