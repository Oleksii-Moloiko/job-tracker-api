def test_register_success(client):
    response = client.post(
        "/auth/register",
        json={
            "email": "newuser@example.com",
            "username": "newuser",
            "password": "strongpassword123",
        },
    )

    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert data["username"] == "newuser"
    assert "id" in data
    assert "created_at" in data


def test_register_duplicate_user(client, test_user):
    response = client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "strongpassword123",
        },
    )

    assert response.status_code == 400


def test_login_success(client, test_user):
    response = client.post(
        "/auth/login",
        data={
            "username": "test@example.com",
            "password": "strongpassword123",
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_password(client, test_user):
    response = client.post(
        "/auth/login",
        data={
            "username": "test@example.com",
            "password": "wrongpassword",
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    assert response.status_code == 401


def test_read_me(client, auth_headers):
    response = client.get("/auth/me", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["username"] == "testuser"


def test_refresh_token_success(client, auth_tokens):
    response = client.post(
        "/auth/refresh",
        json={
            "refresh_token": auth_tokens["refresh_token"]
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


def test_logout_revokes_refresh_token(client, auth_tokens):
    logout_response = client.post(
        "/auth/logout",
        json={
            "refresh_token": auth_tokens["refresh_token"]
        },
    )

    assert logout_response.status_code == 204

    refresh_response = client.post(
        "/auth/refresh",
        json={
            "refresh_token": auth_tokens["refresh_token"]
        },
    )

    assert refresh_response.status_code == 401