def test_edit_get(client):
    with client.session_transaction() as sess:
        sess["user_id"] = 1

    response = client.get("/edit/1")

    assert response.status_code in [200, 302]