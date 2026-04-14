# Teste para verificar o comportamento do filtro de lançamentos quando não há resultados
def test_filtro_sem_resultado(app_context):
    from app.services.services import filtrar_lancamentos


    resultado = filtrar_lancamentos(1, "2020-01-01", "2020-01-02")
    
    assert len(resultado) == 0