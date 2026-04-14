# Teste para verificar o filtro por data no dashboard (HTML)
def test_filtro_por_data(client):
    from app.models import db, Lancamento
    from datetime import date

    with client.application.app_context():
        db.session.query(Lancamento).delete()

        db.session.add_all([
            Lancamento(descricao="Ontem", valor=100, tipo="R", usuario_id=1, data=date(2026,3,26), status=True),
            Lancamento(descricao="Hoje", valor=200, tipo="R", usuario_id=1, data=date(2026,3,27), status=True),
        ])
        db.session.commit()

    with client.session_transaction() as sess:
        sess["user_id"] = 1

    response = client.get("/dashboard?data_inicio=2026-03-27&data_fim=2026-03-27")

    html = response.data.decode()

    assert "Hoje" in html
    assert "Ontem" not in html