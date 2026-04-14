# Teste para o filtro de lançamentos somente a partir de uma data de início
def test_filtro_somente_inicio(app_context):
    from app.services.services import filtrar_lancamentos

    resultado = filtrar_lancamentos(1, "2026-01-01", None)

    assert isinstance(resultado, list)