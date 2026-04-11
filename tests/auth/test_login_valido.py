# Teste de Login Válido
def test_login_valido(client):
    response = client.post("/", data={
        "login": "admin",
        "senha": "123"
    })

    assert response.status_code == 302