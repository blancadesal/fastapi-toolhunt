def test_ping(test_app):
    response = test_app.get("/api/v1/ping")
    assert response.status_code == 200
    assert response.json() == {"environment": "dev", "ping": "pong!", "testing": True}
