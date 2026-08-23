"""/hello1 エンドポイントのテスト。"""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_hello1_returns_200_and_message() -> None:
    """GET /hello1 が200と {"message": "Hello1"} を返すことを確認する（REQ-001）。"""
    response = client.get("/hello1")

    assert response.status_code == 200
    assert response.json() == {"message": "Hello1"}


def test_get_undefined_path_returns_404() -> None:
    """未定義パスへのGETリクエストが404を返すことを確認する（REQ-002）。"""
    response = client.get("/undefined")

    assert response.status_code == 404


def test_post_hello1_returns_405() -> None:
    """/hello1 へのPOSTリクエストが405を返すことを確認する（REQ-003）。"""
    response = client.post("/hello1")

    assert response.status_code == 405
