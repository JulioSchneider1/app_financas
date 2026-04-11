# Teste para verificar se a rota de adicionar redireciona corretamente após a adição de um registro.
def test_add_redirect(client):
    with client.session_transaction() as sess:
        sess["user_id"] = 1

    response = client.post("/add", data={
        "descricao": "Teste",
        "valor": 10,
        "tipo": "R"
    })

    assert response.status_code == 302