"""GET /hello1 エンドポイントを提供するルーター。"""

from fastapi import APIRouter

from app.schemas import HelloResponse

router = APIRouter(prefix="/hello1", tags=["hello1"])


@router.get("", response_model=HelloResponse)
def get_hello1() -> HelloResponse:
    """
    Summary:
        /hello1 へのGETリクエストに対しHello1を返す。

    Args:
        None

    Returns:
        HelloResponse: message フィールドに "Hello1" を含むレスポンス。
    """
    return HelloResponse(message="Hello1")
