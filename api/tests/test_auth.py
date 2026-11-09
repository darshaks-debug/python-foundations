def test_register_user(client):
    response = client.post("/register", json={"username": "testuser", "password": "password123"})
    assert response.status_code == 200
    assert response.json()["message"] == "User created successfully"

def test_register_duplicate_user(client):
    # Register once
    client.post("/register", json={"username": "testuser", "password": "password123"})
    # Try again
    response = client.post("/register", json={"username": "testuser", "password": "password123"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Username already registered"

def test_login_success(client):
    client.post("/register", json={"username": "testuser", "password": "password123"})
    response = client.post("/token", data={"username": "testuser", "password": "password123"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_failure(client):
    response = client.post("/token", data={"username": "wronguser", "password": "wrongpass"})
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"