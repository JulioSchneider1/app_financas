def test_filtro_somente_inicio(app_context):
    from app import filtrar_lancamentos, app

    with app.app_context():
        resultado = filtrar_lancamentos(1, "2026-01-01", None)
        assert isinstance(resultado, list)