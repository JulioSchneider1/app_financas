# Teste para a função de cálculo de saldo
def test_calculo_saldo():
    from app import calcular_totais
    from models import Lancamento

    lancamentos = [
        Lancamento(valor=100, tipo="R", status=True),
        Lancamento(valor=50, tipo="D", status=True),
    ]

    receitas, despesas, saldo = calcular_totais(lancamentos)

    assert saldo == 50