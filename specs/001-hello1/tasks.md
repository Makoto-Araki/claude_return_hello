# Tasks: /hello1 エンドポイント

対応するドキュメント: requirements.md, design.md

## タスク一覧

- [x] TASK-1: プロジェクトの初期化
  - `uv init` でpyproject.tomlを作成
  - `uv add fastapi uvicorn` で依存関係を追加
  - `uv add --dev pytest ruff` で開発用依存関係を追加

- [x] TASK-2: レスポンスモデルの定義
  - `app/routers/hello1.py` に Pydantic `BaseModel`（`HelloResponse`）を定義
  - フィールド: `message: str`

- [x] TASK-3: GET /hello1 ハンドラの実装
  - `app/routers/hello1.py` に `APIRouter` を用いてGETハンドラを実装
  - Google style Docstringを付与（CLAUDE.md準拠）
  - 対応要件: REQ-001

- [x] TASK-4: ルーターの登録
  - `app/main.py` にFastAPIインスタンスを生成
  - `hello1.router` を `include_router` で登録

- [x] TASK-5: テストコードの作成
  - `tests/test_hello1.py` に `TestClient` を用いたテストを実装
  - GET /hello1 → 200, `{"message": "Hello1"}`（REQ-001）
  - GET /undefined → 404（REQ-002）
  - POST /hello1 → 405（REQ-003）

- [x] TASK-6: 動作確認
  - `uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000` でサーバー起動
  - `curl http://localhost:8000/hello1` で200と `{"message":"Hello1"}` を確認

- [x] TASK-7: 品質チェック
  - `uv run ruff check .` がエラーなしで通過することを確認
  - `uv run pytest` が全件パスすることを確認

## 完了条件
requirements.mdの受け入れ基準をすべて満たし、TASK-1〜TASK-7がすべて完了して
いること。
