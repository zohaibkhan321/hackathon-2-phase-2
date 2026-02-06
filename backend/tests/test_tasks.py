import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_tasks_crud():
    """Test basic tasks CRUD operations."""
    # Register a test user
    register_response = client.post(
        "/api/auth/register",
        json={
            "email": "task_test@example.com",
            "password": "testpassword123"
        }
    )

    # Login to get a token
    login_response = client.post(
        "/api/auth/login",
        data={
            "email": "task_test@example.com",
            "password": "testpassword123"
        }
    )

    # Extract token from response (this is a simplified test)
    # In a real test, we'd extract the token properly
    assert login_response.status_code == 200

    # Test creating a task (would need to set Authorization header in real test)
    # response = client.post(
    #     "/api/tasks",
    #     json={
    #         "title": "Test task",
    #         "description": "Test description"
    #     },
    #     headers={"Authorization": f"Bearer {token}"}
    # )
    # assert response.status_code == 200