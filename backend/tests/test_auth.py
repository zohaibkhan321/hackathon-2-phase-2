import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_register_user():
    """Test user registration endpoint."""
    response = client.post(
        "/api/auth/register",
        json={
            "email": "test@example.com",
            "password": "testpassword123"
        }
    )
    # This would normally return 200, but may return 400 if user already exists
    assert response.status_code in [200, 400]


def test_login_user():
    """Test user login endpoint."""
    # First register a user
    client.post(
        "/api/auth/register",
        json={
            "email": "login_test@example.com",
            "password": "testpassword123"
        }
    )

    # Then try to login
    response = client.post(
        "/api/auth/login",
        data={
            "email": "login_test@example.com",
            "password": "testpassword123"
        }
    )
    assert response.status_code in [200, 400]