"""複数のルーター間で共有するレスポンススキーマ。"""

from pydantic import BaseModel


class HelloResponse(BaseModel):
    """hello系エンドポイントの共通レスポンスモデル。

    Attributes:
        message: 返却するメッセージ文字列。
    """

    message: str
