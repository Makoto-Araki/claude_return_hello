# Design: /hello2 エンドポイント

対応する要件: requirements.md（REQ-001〜REQ-003）

## アーキテクチャ
hello1と同一のFastAPI + uvicorn構成を踏襲する。エンドポイントは
`app/routers/` 配下にファイル分割し、`app/main.py` で集約登録する
（CLAUDE.mdの規約に準拠）。

## ディレクトリ構成
```
app/
├── main.py               # hello1.router に加え hello2.router を登録
├── schemas.py            # 新規追加：HelloResponse を共通定義として切り出す
└── routers/
    ├── hello1.py         # 変更あり：HelloResponseの定義をschemas.pyに移し、import に変更
    └── hello2.py         # 新規追加：schemas.py の HelloResponse を import して使用

tests/
├── test_hello1.py        # 既存（変更なし、リグレッション確認のみ）
└── test_hello2.py        # 新規追加
```

## コンポーネント設計

### app/schemas.py（新規）
- `HelloResponse` を共通のレスポンスモデルとしてここに定義する
  - フィールド: `message: str`
  - Google style Docstringを付与する

### app/routers/hello1.py（改修）
- `HelloResponse` の定義を削除し、`from app.schemas import HelloResponse` に置き換える
- ハンドラの実装・振る舞いは変更しない（回帰リスクを最小化するため、
  importの変更のみに留める）

### app/routers/hello2.py（新規）
- `APIRouter` を用いて `/hello2` のGETハンドラを定義する
- `from app.schemas import HelloResponse` でレスポンス型を利用する
- ハンドラ関数にはGoogle style Docstringを付与する（CLAUDE.md準拠）

### app/main.py
- 既存の `hello1.router` に加え、`hello2.router` を `include_router` で登録する

## エンドポイント仕様
| Method | Path    | リクエスト | レスポンス（200）        | エラー時                    |
|--------|---------|------------|---------------------------|------------------------------|
| GET    | /hello2 | なし       | `{"message": "Hello2"}`   | 未定義パス→404、他メソッド→405 |

404/405はFastAPIの標準ルーティング機構により自動的にハンドリングされるため、
個別の例外ハンドラは実装しない（hello1と共通の挙動）。

## テスト設計（tests/test_hello2.py）
`TestClient` を用いて以下をテストする。
- REQ-001対応: GET /hello2 → 200, `{"message": "Hello2"}`
- REQ-002対応: GET /undefined → 404
- REQ-003対応: POST /hello2 → 405
- 回帰確認: GET /hello1 → 200（既存機能への影響がないことの確認）

## 技術的決定事項
- `HelloResponse` モデルは `app/schemas.py` に共通化する。hello2実装の
  タイミングで前倒しして切り出すことで、hello3以降も同じ共通モジュールを
  利用できる
- hello1.py の改修はimport文の変更のみに限定し、ロジックや振る舞いには
  一切手を加えない。既存テスト（test_hello1.py）がすべてパスすることを
  リグレッション確認の基準とする
- 将来の `/hello3` 追加時、本設計を踏まえたhello2.pyをテンプレートとして扱う
