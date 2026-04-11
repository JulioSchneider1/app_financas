# Teste para verificar se a rota "/dashboard" redireciona para a página de login quando o usuário não está autenticado.
def test_dashboard_sem_login(client):
    response = client.get("/dashboard")
    assert response.status_code == 302