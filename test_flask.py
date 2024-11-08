# import pytest
# import pytest_asyncio
# from httpx import AsyncClient
from main import app
from fastapi.testclient import TestClient


client = TestClient(app)


def test_first_test():
    assert 1 == 1
    # assert response.json() == {"msg": "Hello World"}


def test_read_main():
    response = client.get("/recipe")
    print("begin response")
    print(response)
    print(f'response.json = {response.json()}')
    print("end response")
    assert response.status_code == 200


def test_read_main2():
    response = client.get("/recipe/1")
    print("begin response")
    print(response)
    print(f'response.json = {response.json()}')
    print("end response")
    assert response.status_code == 200
    assert response.json()['id'] == 1


def test_create_reciple() -> None:
    headers = {"Content-Type": "application/json"}
    user_data = {"name": "Никита", "views": 2, "time": 9}
    response = client.post("/recipe", headers=headers, json=user_data)
    print(f'response.json = {response.json()}')

    assert response.status_code == 200

def test_create_parking() -> None:
    user_data = {"name": "Никита", "views": 2, "time": 9}
    response = client.post("/recipe/", headers={"Content-Type": "application/json"}, json=user_data)
    print(f'response.json = {response.json()}')
    assert response.status_code == 200


# async def test_get_specific_operations(ac: AsyncClient):
#     response = await ac.get("http://127.0.0.1:8000/recipe/",)
#
#     assert response.status_code == 200
#     assert response.json()["status"] == "success"
#     assert len(response.json()["data"]) == 1
#
#
# def test_read_all_item():
#     response = client.get("/recipe/", headers={"X-Token": "coneofsilence"})
#     assert response.status_code == 200
#
#
# def test_read_item():
#     response = client.get("/recipe/1/", headers={"X-Token": "coneofsilence"})
#     assert response.status_code == 200
#     assert response.json() == {
#         "id": 1,
#         "name": "first",
#     }

