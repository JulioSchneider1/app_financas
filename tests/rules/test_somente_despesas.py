# Teste para verificar se o cálculo de despesas está correto quando há apenas despesas.
def test_somente_despesas():
    from app import calcular_totais
    from app.models import Lancamento

    lancamentos = [
        Lancamento(valor=100, tipo="D", status=True),
    ]

    _, despesas, _ = calcular_totais(lancamentos)

    assert despesas == 100