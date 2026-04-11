def test_dashboard_com_login(client):
    with client.session_transaction() as sess:
        sess["user_id"] = 1

    response = client.get("/dashboard")

    assert response.status_code == 200