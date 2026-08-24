# Requirements: /hello2 エンドポイント

## 背景・目的
CLAUDE.mdの規約に基づき、hello1で確立した実装パターンを踏襲して2つ目の
エンドポイントを追加する。

## スコープ
- 対象: GET /hello2 エンドポイントの実装
- 対象外: hello3（着手時に別途requirements.mdを作成する）

## 機能要件（EARS形式）
- REQ-001: システムは GET /hello2 リクエストを受け取ったとき、
  ステータスコード200と共にJSON {"message": "Hello2"} を返さなければならない。
- REQ-002: システムは /hello2 以外の未定義パスへのGETリクエストに対しては
  404を返さなければならない（既存のhello1実装と共通の挙動）。
- REQ-003: システムは /hello2 に対してGET以外のHTTPメソッド
  （POST, PUT, DELETE等）を受け取ったとき、405を返さなければならない。

## 非機能要件
- レスポンスタイムは通常時100ms以内
- 認証・認可は不要（公開エンドポイント）
- リクエストパラメータ・リクエストボディは受け付けない
- 既存の /hello1 エンドポイントの挙動に影響を与えないこと

## 受け入れ基準
- [x] `curl http://localhost:8000/hello2` が200と `{"message":"Hello2"}` を返す
- [x] `curl -X POST http://localhost:8000/hello2` が405を返す
- [x] `curl http://localhost:8000/hello1` が引き続き200を返す（既存機能への
  影響がないことの確認）
- [x] pytestによる自動テストが存在し、上記のケースをカバーする
- [x] `uv run ruff check .` がエラーなしで通過する

## 今後の拡張との関係
本要件も hello1 と同様、CLAUDE.mdの規約（1エンドポイント=1ファイル、
Google style Docstring等）に従う。hello3実装時のテンプレートとしても扱う。
