def test_criar_lancamento_sem_login(client):
    response = client.post("/add", data={
        "descricao": "Teste",
        "valor": 10,
        "tipo": "R"
    })

    assert response.status_code == 302