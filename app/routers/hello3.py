"""GET /hello3 エンドポイントを提供するルーター。"""

from fastapi import APIRouter

from app.schemas import HelloResponse

router = APIRouter(prefix="/hello3", tags=["hello3"])


@router.get("", response_model=HelloResponse)
def get_hello3() -> HelloResponse:
    """
    Summary:
        /hello3 へのGETリクエストに対しHello3を返す。

    Args:
        None

    Returns:
        HelloResponse: message フィールドに "Hello3" を含むレスポンス。
    """
    return HelloResponse(message="Hello3")
