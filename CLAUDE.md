# CLAUDE.md

このファイルはClaude Codeがセッション開始時に読み込む、プロジェクト固有の設定です。

## プロジェクト概要
Dev Container上で動作するシンプルなAPIサーバー。GET `/hello1` にリクエストすると
`Hello1` を返す。今後 `/hello2`, `/hello3` ... と同じパターンでエンドポイントを
追加していく学習用プロジェクト。

## 技術スタック
- Python 3.12
- FastAPI + uvicorn
- パッケージ管理: uv（`uv add`, `uv run`）
- テスト: pytest

## よく使うコマンド
- 依存関係インストール: `uv sync`
- サーバー起動: `uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`
- テスト実行: `uv run pytest`
- ruffの依存関係追加: `uv add --dev ruff`
- 静的解析（lint）: `uv run ruff check .`
- フォーマット: `uv run ruff format .`
- 動作確認: `curl http://localhost:8000/hello1`

## ディレクトリ構成とエンドポイント追加の規約
エンドポイントは1機能1ファイルで `app/routers/` 配下に配置し、`app/main.py` で
`include_router` して集約する。新しいエンドポイント（例: hello2, hello3）を
追加する際は、既存の `app/routers/hello1.py` と同じ構造をコピーして流用すること。

```
app/
├── main.py               # FastAPIインスタンス生成、各routerの登録
└── routers/
    ├── hello1.py         # GET /hello1 -> {"message": "Hello1"}
    ├── hello2.py         # GET /hello2 -> {"message": "Hello2"}（追加予定）
    └── hello3.py         # GET /hello3 -> {"message": "Hello3"}（追加予定）

tests/
├── test_hello1.py
├── test_hello2.py        # 追加予定
└── test_hello3.py        # 追加予定
```

## エンドポイント実装の統一パターン
- レスポンスは Pydantic の `BaseModel` で型定義する（例: `HelloResponse`）
- パス名とレスポンスメッセージは対応させる（`/helloN` → `{"message": "HelloN"}`）
- 各エンドポイントには対応するpytestテストを必ず作成する
- ルーターのprefixやtagは `hello1`, `hello2` ... の連番に合わせて命名する

## コーディング規約
- 関数・変数名は英語のsnake_case
- 型ヒントを必須とする
- 1エンドポイント = 1ファイル、1テストファイルの原則を守る
- すべての関数・エンドポイントにDocstringを記述する（Google style）
  - Summary、Args、Returnsを最低限含める
  - 例:
    ```python
    def get_hello1() -> HelloResponse:
        """
        Summary:
            /hello1 へのGETリクエストに対しHello1を返す。

        Args:
            None

        Returns:
            HelloResponse: message フィールドに "Hello1" を含むレスポンス。
        """
    ```

## 注意事項
- .env に秘匿情報を書く場合はコミットしない（.gitignore済み）
- 新規エンドポイント追加時は、既存実装との一貫性（命名・構造）を優先する
- 実装完了とみなす条件: `uv run ruff check .` がエラーなしで通過し、かつ `uv run pytest` が全件パスすること
