from fastapi.testclient import TestClient


def test_import_router_valid_file(client: TestClient):
    response = client.post(
        url="/api/imports/",
        files={"file": ("test.csv", b"name,age\nAna,30", "text/csv")},
    )
    assert response.status_code == 202
    assert response.json() == {"import_id": 123, "status": "pending"}


def test_import_router_invalid_file(client: TestClient):
    response = client.post(
        url="/api/imports/",
        files={"file": ("test.txt", b"name,age\nAna,30", "text/txt")},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid file extension"}
