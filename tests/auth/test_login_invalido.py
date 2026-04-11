# Teste de Login Inválido
def test_login_invalido(client):
    response = client.post("/", data={
        "login": "errado",
        "senha": "errado"
    })

    assert response.status_code == 200