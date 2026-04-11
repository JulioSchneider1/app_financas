# Teste para verificar o comportamento ao tentar deletar um lançamento inexistente
def test_delete_inexistente(client):
    with client.session_transaction() as sess:
        sess["user_id"] = 1

    response = client.get("/delete/999")

    assert response.status_code == 302