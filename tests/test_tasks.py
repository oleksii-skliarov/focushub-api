def test_create_task_success(auth_client):
    response = auth_client.post(
        "/tasks",
        json={
            "title": "Test Task",
            "completed": False,
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["completed"] is False
    assert "id" in data


def test_get_tasks_success(auth_client):
    auth_client.post(
        "/tasks",
        json={
            "title": "My Task",
            "completed": False,
        },
    )
    response = auth_client.get("/tasks")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["title"] == "My Task"


def test_get_tasks_unauthorized(client):
    response = client.get("/tasks")
    assert response.status_code == 401