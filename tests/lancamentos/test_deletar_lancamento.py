# Teste para deletar um lançamento
def test_deletar_lancamento(client):
    from models import db, Lancamento

    with client.application.app_context():
        lanc = Lancamento(descricao="Teste", valor=10, tipo="R", usuario_id=1)
        db.session.add(lanc)
        db.session.commit()
        lanc_id = lanc.id

    with client.session_transaction() as sess:
        sess["user_id"] = 1

    response = client.get(f"/delete/{lanc_id}")

    assert response.status_code == 302