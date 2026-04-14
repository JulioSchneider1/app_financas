# Teste para verificar a contagem de lançamentos filtrados por data
def test_filtro_por_data_count(app_context):
    from app.services.services import filtrar_lancamentos
    from app.models import db, Lancamento
    from datetime import date

    db.session.query(Lancamento).delete()

    db.session.add_all([
        Lancamento(descricao="A", valor=10, tipo="R", usuario_id=1, data=date(2026,3,26), status=True),
        Lancamento(descricao="B", valor=20, tipo="R", usuario_id=1, data=date(2026,3,27), status=True),
    ])
    db.session.commit()

    resultado = filtrar_lancamentos(1, date(2026,3,27), date(2026,3,27))

    assert len(resultado) == 1