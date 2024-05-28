def test_ping(test_app):
    response = test_app.get("/api/v1/ping")
    assert response.status_code == 200
    assert response.json() == {
        "environment": "dev",
        "ping": "pong!",
        "testing": True,
        "database_url": "mysql://user:mypassword@db:3306/web_test?charset=utf8mb4",
        "toolhub_api_endpoint": "https://toolhub-demo.wmcloud.org/api/tools/",
    }
