def test_saldo_ignora_pendentes():
    from app import calcular_totais
    from models import Lancamento

    lancamentos = [
        Lancamento(valor=100, tipo="R", status=True),
        Lancamento(valor=500, tipo="R", status=False),
    ]

    receitas, _, _ = calcular_totais(lancamentos)

    assert receitas == 100