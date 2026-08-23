"""/hello1 エンドポイントのテスト。"""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_hello1_returns_200_and_message() -> None:
    """
    Summary:
        GET /hello1 が200と {"message": "Hello1"} を返すことを確認する（REQ-001）。

    Args:
        None

    Returns:
        None
    """
    response = client.get("/hello1")

    assert response.status_code == 200
    assert response.json() == {"message": "Hello1"}


def test_get_undefined_path_returns_404() -> None:
    """
    Summary:
        未定義パスへのGETリクエストが404を返すことを確認する（REQ-002）。

    Args:
        None

    Returns:
        None
    """
    response = client.get("/undefined")

    assert response.status_code == 404


def test_post_hello1_returns_405() -> None:
    """
    Summary:
        /hello1 へのPOSTリクエストが405を返すことを確認する（REQ-003）。

    Args:
        None

    Returns:
        None
    """
    response = client.post("/hello1")

    assert response.status_code == 405
