# Teste para verificar a criação de um lançamento financeiro
def test_criar_lancamento(client):
    from models import db, Lancamento

    with client.session_transaction() as sess:
        sess["user_id"] = 1

    response = client.post("/add", data={
        "descricao": "Teste",
        "valor": 50,
        "tipo": "R"
    })

    assert response.status_code == 302