# Requirements: /hello1 エンドポイント

## 背景・目的
Dev Container + Claude Code による開発フローの検証を目的とした、最小構成のAPI
エンドポイントを実装する。本機能はhello2, hello3への拡張を見据えた最初の
テンプレートとなる。

## スコープ
- 対象: GET /hello1 エンドポイントの実装
- 対象外: hello2, hello3（着手時に別途requirements.mdを作成する）

## 機能要件（EARS形式）
- REQ-001: システムは GET /hello1 リクエストを受け取ったとき、
  ステータスコード200と共にJSON {"message": "Hello1"} を返さなければならない。
- REQ-002: システムは /hello1 以外の未定義パスへのGETリクエストに対しては
  404を返さなければならない。
- REQ-003: システムは /hello1 に対してGET以外のHTTPメソッド
  （POST, PUT, DELETE等）を受け取ったとき、405を返さなければならない。

## 非機能要件
- レスポンスタイムは通常時100ms以内
- 認証・認可は不要（公開エンドポイント）
- リクエストパラメータ・リクエストボディは受け付けない

## 受け入れ基準
- [x] `curl http://localhost:8000/hello1` が200と `{"message":"Hello1"}` を返す
- [x] `curl -X POST http://localhost:8000/hello1` が405を返す
- [x] `curl http://localhost:8000/undefined` が404を返す
- [x] pytestによる自動テストが存在し、上記3ケースをカバーする
- [x] `uv run ruff check .` がエラーなしで通過する

## 今後の拡張との関係
本要件で確定する実装パターン（ディレクトリ構成、レスポンスモデル、テスト構成）
は、CLAUDE.mdの規約に従い hello2, hello3 でもそのまま踏襲する。
