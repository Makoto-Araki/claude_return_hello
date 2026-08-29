# Design: /hello3 エンドポイント

対応する要件: requirements.md（REQ-001〜REQ-003）

## アーキテクチャ
hello1・hello2と同一のFastAPI + uvicorn構成を踏襲する。エンドポイントは
`app/routers/` 配下にファイル分割し、`app/main.py` で集約登録する
（CLAUDE.mdの規約に準拠）。

## ディレクトリ構成
```
app/
├── main.py               # hello1.router, hello2.router に加え hello3.router を登録
├── schemas.py             # 既存（変更なし）：HelloResponse をそのまま再利用
└── routers/
    ├── hello1.py          # 既存（変更なし）
    ├── hello2.py           # 既存（変更なし）
    └── hello3.py           # 新規追加

tests/
├── test_hello1.py         # 既存（変更なし）
├── test_hello2.py          # 既存（変更なし）
└── test_hello3.py          # 新規追加
```

## コンポーネント設計

### app/routers/hello3.py（新規）
- `APIRouter` を用いて `/hello3` のGETハンドラを定義する
- `from app.schemas import HelloResponse` でレスポンス型を利用する
  （hello2と同様、既存の共通スキーマをそのまま再利用。新規定義や改修は不要）
- ハンドラ関数にはGoogle style Docstringを付与する（CLAUDE.md準拠）

### app/main.py（改修）
- 既存の `hello1.router`, `hello2.router` の登録はそのまま維持し、
  `hello3.router` を `include_router` で追加登録する

## エンドポイント仕様
| Method | Path    | リクエスト | レスポンス（200）        | エラー時                    |
|--------|---------|------------|---------------------------|------------------------------|
| GET    | /hello3 | なし       | `{"message": "Hello3"}`   | 未定義パス→404、他メソッド→405 |

404/405はFastAPIの標準ルーティング機構により自動的にハンドリングされるため、
個別の例外ハンドラは実装しない（既存実装と共通の挙動）。

## テスト設計（tests/test_hello3.py）
`TestClient` を用いて以下をテストする。
- REQ-001対応: GET /hello3 → 200, `{"message": "Hello3"}`
- REQ-002対応: GET /undefined → 404
- REQ-003対応: POST /hello3 → 405
- 回帰確認: GET /hello1 → 200
- 回帰確認: GET /hello2 → 200

## 技術的決定事項
- hello2実装時に `app/schemas.py` へ共通化済みの `HelloResponse` をそのまま
  利用するため、今回はスキーマ定義・既存ファイルの改修が一切不要
- `app/main.py` への1行追加（`include_router`）以外、既存コードへの変更は
  発生しない見込み。これによりリグレッションリスクはhello2実装時より低い
