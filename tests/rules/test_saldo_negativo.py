# Teste para verificar se o saldo negativo é calculado corretamente
def test_saldo_negativo():
    from app.services.services import calcular_totais
    from app.models import Lancamento

    lancamentos = [
        Lancamento(valor=50, tipo="D", status=True),
    ]

    _, _, saldo = calcular_totais(lancamentos)

    assert saldo < 0