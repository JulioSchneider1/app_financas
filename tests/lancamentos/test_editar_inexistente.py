def test_editar_inexistente(client):
    with client.session_transaction() as sess:
        sess["user_id"] = 1

    response = client.get("/edit/999")

    assert response.status_code in [200, 302]