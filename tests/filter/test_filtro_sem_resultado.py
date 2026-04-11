def test_filtro_sem_resultado(app_context):
    from app import filtrar_lancamentos, app

    with app.app_context():
        resultado = filtrar_lancamentos(1, "2020-01-01", "2020-01-02")
        assert len(resultado) == 0