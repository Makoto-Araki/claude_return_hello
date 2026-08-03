# claude_return_hello

"Hello" と出力するだけのシンプルなプログラムを、Docker Desktop の Kubernetes 上で CronJob として1時間ごとに実行するサンプルです。

## 構成

```
.
├── src/
│   └── hello.py            # アプリ本体
├── tests/
│   └── test_hello.py       # hello.py のテスト
├── requirements-dev.txt    # テスト実行用の開発依存（pytest）
├── k8s/
│   └── cronjob.yaml         # Namespace + CronJob マニフェスト（namespace: claude-sample）
├── .github/
│   └── workflows/           # CI/CD ワークフロー
├── .devcontainer/
│   └── devcontainer.json    # 開発用devcontainer定義
└── Dockerfile
```

## ビルド

Docker Desktop の Kubernetes は同じ Docker デーモンを共有しているため、レジストリへの push は不要です。

```bash
docker build -t claude-return-hello:latest .
```

## デプロイ

`k8s/cronjob.yaml` には `claude-sample` Namespaceの定義も含まれているため、`kubectl apply` 一度で namespace ごと作成されます。

```bash
kubectl apply -f k8s/cronjob.yaml
kubectl get cronjob -n claude-sample
```

## 動作確認

スケジュール（毎時0分）を待たずに手動実行する場合:

```bash
kubectl create job --from=cronjob/hello-cronjob hello-test -n claude-sample
kubectl logs job/hello-test -n claude-sample
```

## テスト

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
pytest -q
```

## CI/CD

GitHub Actions で以下の3つのワークフローを実行します（`.github/workflows/`）。

| ワークフロー | トリガー | 内容 |
| --- | --- | --- |
| `pr-test.yml` | PR作成・更新時（`main`向け） | pytest を実行 |
| `main-ci.yml` | `main` へのpush（マージ）時 | pytest を実行 → Dockerイメージをビルドし Trivy で脆弱性スキャン（CRITICALのみ失敗、HIGH以下はレポートのみ） |
| `release.yml` | `v*` 形式のタグをpushした時 | pytest を実行 → Dockerイメージをビルド → Docker Hub（`makotoaraki346/claude-return-hello`）にタグ名と `latest` の2つのタグでpush |

リリースする場合は、mainマージ後に以下のように次のバージョンのタグをpushします（例: 現時点の最新リリースは `v1.0.2`）。

```bash
git tag v1.0.3
git push origin v1.0.3
```

事前に、リポジトリのSecretsに `DOCKERHUB_USERNAME` と `DOCKERHUB_TOKEN`（Docker Hubのアクセストークン）を登録しておく必要があります。

## ライセンス

[MIT License](./LICENSE)

## 開発の進め方

このリポジトリでの変更は、GitHub Issue を起票してからブランチを切り、実装・動作確認の後に PR を作成してレビュー・マージする流れを基本としています（Issue/PRテンプレート類は、リポジトリの規模に見合わないため導入していません）。CI/CDについては上記の「CI/CD」を参照してください。
