def get_auth_token(client, username, password):
    """Helper function to log in and get the JWT token."""
    client.post("/register", json={"username": username, "password": password})
    response = client.post("/token", data={"username": username, "password": password})
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_add_expense_unauthorized(client):
    response = client.post("/expenses", json={"amount": 100, "description": "Lunch"})
    assert response.status_code == 401 # No token provided

def test_add_expense_with_auth(client):
    headers = get_auth_token(client, "user1", "pass1")
    response = client.post("/expenses", json={"amount": 100, "description": "Pizza"}, headers=headers)
    assert response.status_code == 200
    assert response.json()["expense"]["amount"] == 100
    assert response.json()["expense"]["description"] == "Pizza"

def test_user_isolation(client):
    # User 1 adds an expense
    headers1 = get_auth_token(client, "user1", "pass1")
    client.post("/expenses", json={"amount": 100, "description": "User 1 Secret"}, headers=headers1)

    # User 2 logs in and checks their list
    headers2 = get_auth_token(client, "user2", "pass2")
    response = client.get("/expenses", headers=headers2)
    
    # User 2 should see an empty list, NOT User 1's expense
    assert response.status_code == 200
    assert len(response.json()) == 0 

    # User 2 tries to delete User 1's expense (ID 1)
    delete_response = client.delete("/expenses/1", headers=headers2)
    assert delete_response.status_code == 404 # Should be Not Found