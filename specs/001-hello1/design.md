# Design: /hello1 エンドポイント

対応する要件: requirements.md（REQ-001〜REQ-003）

## アーキテクチャ
FastAPI + uvicornによるシングルサービス構成。エンドポイントは
`app/routers/` 配下にファイル分割し、`app/main.py` で集約登録する
（CLAUDE.mdの規約に準拠）。

## ディレクトリ構成
```
app/
├── main.py                # FastAPIインスタンス生成、routerの登録
└── routers/
    └── hello1.py          # GET /hello1 の実装

tests/
└── test_hello1.py
```

## コンポーネント設計

### app/routers/hello1.py
- `APIRouter` を用いて `/hello1` のGETハンドラを定義する
- レスポンス型は Pydantic `BaseModel`（`HelloResponse`）で定義する
  - フィールド: `message: str`
- ハンドラ関数にはGoogle style Docstringを付与する（CLAUDE.md準拠）

### app/main.py
- FastAPIインスタンスを生成し、`hello1.router` を `include_router` で登録する
- 今後 `hello2`, `hello3` を追加する際も同様に `include_router` を並べる想定

## エンドポイント仕様
| Method | Path    | リクエスト | レスポンス（200）        | エラー時                    |
|--------|---------|------------|---------------------------|------------------------------|
| GET    | /hello1 | なし       | `{"message": "Hello1"}`   | 未定義パス→404、他メソッド→405 |

404/405はFastAPIの標準ルーティング機構により自動的にハンドリングされるため、
個別の例外ハンドラは実装しない。

## テスト設計（tests/test_hello1.py）
`TestClient`（FastAPIのテストユーティリティ）を用いて以下をテストする。
- REQ-001対応: GET /hello1 → 200, `{"message": "Hello1"}`
- REQ-002対応: GET /undefined → 404
- REQ-003対応: POST /hello1 → 405

## 技術的決定事項
- レスポンスモデルを型定義することで、OpenAPIスキーマ（Swagger UI）にも
  自動反映させる
- 将来の `/hello2`, `/hello3` 追加時、本設計の `hello1.py` をそのまま
  複製・改変するテンプレートとして扱う（CLAUDE.mdの規約に準拠）
