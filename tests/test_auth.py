

def test_create_user_success(client):
    response = client.post(
        "/users/",
        json={
            "username": "alex_test",
            "email": "alex@example.com",
            "password": "secretpassword123",
        }
    )

    assert response.status_code == 201

    data = response.json()
    assert data["username"] == "alex_test"
    assert data["email"] == "alex@example.com"
    assert "id" in data
    assert "password" not in data

def test_create_invalid_email(client):
    response = client.post(
        "/users/",
        json={
            "username": "bad_email_user",
            "email": "not-an-email-at-all",
            "password": "valid_password123",
        }
    )
    assert response.status_code == 422
    errors = response.json()
    assert "detail" in errors

def test_login_success(client):
    client.post("/users/",
                json={
                    "username": "alex_test",
                    "email": "alex@example.com",
                    "password": "secretpassword123"
                }
                )
    response = client.post(
        "/token",
        data={
            "username": "alex_test",
            "password": "secretpassword123",
        }
    )
    assert response.status_code == 200

    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

