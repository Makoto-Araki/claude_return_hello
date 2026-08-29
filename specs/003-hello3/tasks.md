# Tasks: /hello3 エンドポイント

対応するドキュメント: requirements.md, design.md

## タスク一覧

- [x] TASK-1: GET /hello3 ハンドラの実装
  - `app/routers/hello3.py` を新規作成
  - `APIRouter` を用いてGETハンドラを実装
  - `app/schemas.py` の `HelloResponse` をimportして使用（新規定義は不要）
  - Google style Docstringを付与（CLAUDE.md準拠）
  - 対応要件: REQ-001

- [x] TASK-2: ルーターの登録
  - `app/main.py` に `hello3.router` を `include_router` で追加登録
  - `hello1.router`, `hello2.router` の登録コードは変更しない

- [x] TASK-3: テストコードの作成
  - `tests/test_hello3.py` に `TestClient` を用いたテストを実装
  - GET /hello3 → 200, `{"message": "Hello3"}`（REQ-001）
  - GET /undefined → 404（REQ-002）
  - POST /hello3 → 405（REQ-003）
  - GET /hello1 → 200（既存機能への回帰確認）
  - GET /hello2 → 200（既存機能への回帰確認）
  - Docstringは Google style（Summary/Args/Returns）で記述する

- [x] TASK-4: 既存テストのリグレッション確認
  - `uv run pytest tests/test_hello1.py tests/test_hello2.py` を実行し、
    TASK-2の変更後も既存テストが全てパスすることを確認する

- [x] TASK-5: 動作確認
  - `uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000` でサーバー起動
  - `curl http://localhost:8000/hello3` で200と `{"message":"Hello3"}` を確認
  - `curl http://localhost:8000/hello1`, `curl http://localhost:8000/hello2` で
    既存動作に影響がないことを確認

- [x] TASK-6: 品質チェック
  - `uv run ruff check .` がエラーなしで通過することを確認
  - `uv run pytest`（test_hello1.py, test_hello2.py, test_hello3.py 全て）が
    全件パスすることを確認

## 完了条件
requirements.mdの受け入れ基準をすべて満たし、TASK-1〜TASK-6がすべて完了して
いること。
