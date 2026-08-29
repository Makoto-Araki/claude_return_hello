# claude-return-hello

Dev Container上で動作するシンプルなAPIサーバー。GET `/hello1` にリクエストする
と `Hello1` を返す。同じパターンで `/hello2`, `/hello3` ... とエンドポイントを
追加していく学習用プロジェクト。

## 技術スタック
- Python 3.12
- FastAPI + uvicorn
- パッケージ管理: uv（`uv add`, `uv run`）
- テスト: pytest / Lint: ruff
- コンテナ: Docker / Kubernetes（Docker Desktop）

## エンドポイント一覧

| Method | Path      | レスポンス（200）         | 対応spec |
|--------|-----------|----------------------------|----------|
| GET    | /hello1   | `{"message": "Hello1"}`    | [specs/001-hello1](specs/001-hello1) |
| GET    | /hello2   | `{"message": "Hello2"}`    | [specs/002-hello2](specs/002-hello2) |
| GET    | /hello3   | `{"message": "Hello3"}`    | [specs/003-hello3](specs/003-hello3) |

いずれも未定義パスへのGETは404、GET以外のメソッドは405を返す。

## ディレクトリ構成

```
app/
├── main.py               # FastAPIインスタンス生成、各routerの登録
├── schemas.py             # 共通レスポンスモデル（HelloResponse）
└── routers/
    ├── hello1.py
    ├── hello2.py
    └── hello3.py

tests/
├── test_hello1.py
├── test_hello2.py
└── test_hello3.py

specs/                     # 機能ごとの requirements.md / design.md / tasks.md
k8s/                        # Kubernetesマニフェスト（namespace, deployment, service）
Dockerfile
```

## ローカル開発

```bash
# 依存関係インストール
uv sync

# サーバー起動
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 動作確認
curl http://localhost:8000/hello1

# テスト実行
uv run pytest

# 静的解析
uv run ruff check .

# フォーマット
uv run ruff format .
```

## Docker Desktop の Kubernetes 上で動かす

ローカルPCのDocker Desktopで有効化したKubernetesクラスタに、専用namespace
（`claude-return-hello`）を作ってDeploymentとして動かす構成。リソース節約を
優先し、`replicas: 1`・最小限のCPU/メモリ requests・limits・単一の
livenessProbeのみというシンプルな構成にしている（[k8s/deployment.yaml](k8s/deployment.yaml)）。

### 前提: イメージストアの設定

Docker DesktopのKubernetesノードは既定では`docker build`のイメージストアと
別管理のcontainerdを持つため、レジストリへのpushなしでローカルイメージを
そのまま使うには以下の設定が必要。

**Docker Desktop → Settings → General → 「Use containerd for pulling and
storing images」を有効化**（設定変更後、Docker Desktopの再起動が必要）

### 手順

```bash
# 1. イメージのビルド
docker build -t claude-return-hello:latest .

# 2. namespace作成
kubectl apply -f k8s/namespace.yaml

# 3. Deployment / Service の適用
kubectl apply -f k8s/deployment.yaml

# 4. ロールアウト完了を待つ
kubectl rollout status deployment/claude-return-hello -n claude-return-hello
```

### 動作確認

```bash
kubectl port-forward service/claude-return-hello -n claude-return-hello 8000:8000
```

別ターミナルで:
```bash
curl http://localhost:8000/hello1
curl http://localhost:8000/hello2
curl http://localhost:8000/hello3
```

### 後片付け

```bash
kubectl delete -f k8s/deployment.yaml
kubectl delete -f k8s/namespace.yaml
```

## 開発フロー（spec駆動）

新しいエンドポイントを追加する際は、`specs/00N-helloN/` 配下に
`requirements.md`（EARS形式の要件） → `design.md`（設計） →
`tasks.md`（タスク分解、完了ごとにチェックボックス更新）の順でドキュメント
を作成してから実装する。実装のコーディング規約・命名規則は [CLAUDE.md](CLAUDE.md)
を参照。
