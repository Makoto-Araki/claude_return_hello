# Requirements: /hello3 エンドポイント

## 背景・目的
CLAUDE.mdの規約に基づき、hello1・hello2で確立した実装パターンを踏襲して
3つ目のエンドポイントを追加する。

## スコープ
- 対象: GET /hello3 エンドポイントの実装
- 対象外: hello4以降（現時点では計画なし）

## 機能要件（EARS形式）
- REQ-001: システムは GET /hello3 リクエストを受け取ったとき、
  ステータスコード200と共にJSON {"message": "Hello3"} を返さなければならない。
- REQ-002: システムは /hello3 以外の未定義パスへのGETリクエストに対しては
  404を返さなければならない（既存実装と共通の挙動）。
- REQ-003: システムは /hello3 に対してGET以外のHTTPメソッド
  （POST, PUT, DELETE等）を受け取ったとき、405を返さなければならない。

## 非機能要件
- レスポンスタイムは通常時100ms以内
- 認証・認可は不要（公開エンドポイント）
- リクエストパラメータ・リクエストボディは受け付けない
- 既存の /hello1, /hello2 エンドポイントの挙動に影響を与えないこと

## 受け入れ基準
- [ ] `curl http://localhost:8000/hello3` が200と `{"message":"Hello3"}` を返す
- [ ] `curl -X POST http://localhost:8000/hello3` が405を返す
- [ ] `curl http://localhost:8000/hello1` が引き続き200を返す（回帰確認）
- [ ] `curl http://localhost:8000/hello2` が引き続き200を返す（回帰確認）
- [ ] pytestによる自動テストが存在し、上記のケースをカバーする
- [ ] `uv run ruff check .` がエラーなしで通過する

## 今後の拡張との関係
hello2で `app/schemas.py` に共通化した `HelloResponse` をそのまま再利用する。
hello1のような改修（import変更）は不要で、hello3は新規ファイルの追加のみで
完結する見込み。
