from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_first_test():
    assert 1 == 1


def test_read_main():
    response = client.get("/recipe")
    print("begin response")
    print(response)
    print(f"response.json = {response.json()}")
    print("end response")
    assert response.status_code == 200


def test_read_main_one():
    response = client.get("/recipe/1")
    print("begin response")
    print(response)
    print(f"response.json = {response.json()}")
    print("end response")
    assert response.status_code == 200
    assert response.json()["id"] == 1


def test_create_reciple() -> None:
    user_data = {"name": "Никита", "views": 2, "time": 9}
    response = client.post(
        "/recipe/",
        headers={"Content-Type": "application/json"}, json=user_data
    )
    print(f"response.json = {response.json()}")
    assert response.status_code == 200
