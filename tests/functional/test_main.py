from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "liamsdemo"}


def test_read_item():
    item_id = 4
    query_param = "newsearch"
    response = client.get(f"/items/{item_id}?q={query_param}")

    assert response.status_code == 200
    assert response.json() == {"item_id": item_id, "q": query_param}
