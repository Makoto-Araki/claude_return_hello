"""/hello3 エンドポイントのテスト。"""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_hello3_returns_200_and_message() -> None:
    """
    Summary:
        GET /hello3 が200と {"message": "Hello3"} を返すことを確認する（REQ-001）。

    Args:
        None

    Returns:
        None
    """
    response = client.get("/hello3")

    assert response.status_code == 200
    assert response.json() == {"message": "Hello3"}


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


def test_post_hello3_returns_405() -> None:
    """
    Summary:
        /hello3 へのPOSTリクエストが405を返すことを確認する（REQ-003）。

    Args:
        None

    Returns:
        None
    """
    response = client.post("/hello3")

    assert response.status_code == 405


def test_get_hello1_still_returns_200() -> None:
    """
    Summary:
        hello3追加後もGET /hello1が200を返すことを確認する（既存機能への回帰確認）。

    Args:
        None

    Returns:
        None
    """
    response = client.get("/hello1")

    assert response.status_code == 200
    assert response.json() == {"message": "Hello1"}


def test_get_hello2_still_returns_200() -> None:
    """
    Summary:
        hello3追加後もGET /hello2が200を返すことを確認する（既存機能への回帰確認）。

    Args:
        None

    Returns:
        None
    """
    response = client.get("/hello2")

    assert response.status_code == 200
    assert response.json() == {"message": "Hello2"}
