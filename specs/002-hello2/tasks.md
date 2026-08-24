# Tasks: /hello2 エンドポイント

対応するドキュメント: requirements.md, design.md

## タスク一覧

- [ ] TASK-1: 共通スキーマの切り出し
  - `app/schemas.py` を新規作成し、`HelloResponse`（`message: str`）を定義
  - Google style Docstringを付与（CLAUDE.md準拠）

- [ ] TASK-2: hello1の改修（リファクタリングのみ）
  - `app/routers/hello1.py` 内の `HelloResponse` の定義を削除
  - `from app.schemas import HelloResponse` に置き換える
  - ハンドラのロジック・振る舞いは変更しない

- [ ] TASK-3: hello1のリグレッション確認
  - `uv run pytest tests/test_hello1.py` を実行し、TASK-2の変更後も
    既存テストが全てパスすることを確認する

- [ ] TASK-4: GET /hello2 ハンドラの実装
  - `app/routers/hello2.py` を新規作成
  - `APIRouter` を用いてGETハンドラを実装
  - `app/schemas.py` の `HelloResponse` をimportして使用
  - Google style Docstringを付与（CLAUDE.md準拠）
  - 対応要件: REQ-001

- [ ] TASK-5: ルーターの登録
  - `app/main.py` に `hello2.router` を `include_router` で追加登録
  - `hello1.router` の登録コードは変更しない

- [ ] TASK-6: テストコードの作成
  - `tests/test_hello2.py` に `TestClient` を用いたテストを実装
  - GET /hello2 → 200, `{"message": "Hello2"}`（REQ-001）
  - GET /undefined → 404（REQ-002）
  - POST /hello2 → 405（REQ-003）
  - GET /hello1 → 200（既存機能への回帰確認）
  - Docstringは Google style（Summary/Args/Returns）で記述する

- [ ] TASK-7: 動作確認
  - `uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000` でサーバー起動
  - `curl http://localhost:8000/hello2` で200と `{"message":"Hello2"}` を確認
  - `curl http://localhost:8000/hello1` で既存動作に影響がないことを確認

- [ ] TASK-8: 品質チェック
  - `uv run ruff check .` がエラーなしで通過することを確認
  - `uv run pytest`（test_hello1.py, test_hello2.py 両方）が全件パスすることを確認

## 完了条件
requirements.mdの受け入れ基準をすべて満たし、TASK-1〜TASK-8がすべて完了して
いること。特にTASK-3のリグレッション確認は、hello1側への意図しない影響が
ないことを保証する重要な工程として省略しないこと。
