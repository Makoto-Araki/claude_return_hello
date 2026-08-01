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
│   └── cronjob.yaml         # Kubernetes CronJobマニフェスト
└── Dockerfile
```

## ビルド

Docker Desktop の Kubernetes は同じ Docker デーモンを共有しているため、レジストリへの push は不要です。

```bash
docker build -t claude-return-hello:latest .
```

## デプロイ

```bash
kubectl apply -f k8s/cronjob.yaml
kubectl get cronjob
```

## 動作確認

スケジュール（毎時0分）を待たずに手動実行する場合:

```bash
kubectl create job --from=cronjob/hello-cronjob hello-test
kubectl logs job/hello-test
```

## テスト

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
pytest -q
```

## 開発の進め方

このリポジトリでの変更は、GitHub Issue を起票してからブランチを切り、実装・動作確認の後に PR を作成してレビュー・マージする流れを基本としています（CI/CD やテンプレート類は、リポジトリの規模に見合わないため導入していません）。
