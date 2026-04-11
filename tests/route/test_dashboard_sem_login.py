def test_dashboard_sem_login(client):
    response = client.get("/dashboard")
    assert response.status_code == 302