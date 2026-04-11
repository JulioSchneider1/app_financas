def test_saldo_negativo():
    from app import calcular_totais
    from models import Lancamento

    lancamentos = [
        Lancamento(valor=50, tipo="D", status=True),
    ]

    _, _, saldo = calcular_totais(lancamentos)

    assert saldo < 0