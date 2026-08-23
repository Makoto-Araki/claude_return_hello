"""GET /hello1 エンドポイントを提供するルーター。"""

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/hello1", tags=["hello1"])


class HelloResponse(BaseModel):
    """/hello1 のレスポンスモデル。

    Attributes:
        message: 返却するメッセージ文字列。
    """

    message: str


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
