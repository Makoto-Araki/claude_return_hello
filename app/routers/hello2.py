"""GET /hello2 エンドポイントを提供するルーター。"""

from fastapi import APIRouter

from app.schemas import HelloResponse

router = APIRouter(prefix="/hello2", tags=["hello2"])


@router.get("", response_model=HelloResponse)
def get_hello2() -> HelloResponse:
    """
    Summary:
        /hello2 へのGETリクエストに対しHello2を返す。

    Args:
        None

    Returns:
        HelloResponse: message フィールドに "Hello2" を含むレスポンス。
    """
    return HelloResponse(message="Hello2")
